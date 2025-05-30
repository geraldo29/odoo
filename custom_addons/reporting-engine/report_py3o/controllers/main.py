# Copyright 2017 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import json
import mimetypes
from urllib.parse import parse_qs

from werkzeug import exceptions
from werkzeug.datastructures import MultiDict

from odoo.http import content_disposition, request, route, serialize_exception
from odoo.tools import html_escape

from odoo.addons.web.controllers.report import ReportController as ReportControllerBase


class ReportController(ReportControllerBase):
    @route()
    def report_routes(self, reportname, docids=None, converter=None, **data):
        if converter != "py3o":
            return super().report_routes(
                reportname=reportname, docids=docids, converter=converter, **data
            )
        context = dict(request.env.context)

        if docids:
            docids = [int(i) for i in docids.split(",")]
        if data.get("options"):
            data.update(json.loads(data.pop("options")))
        if data.get("context"):
            # Ignore 'lang' here, because the context in data is the
            # one from the webclient *but* if the user explicitely wants to
            # change the lang, this mechanism overwrites it.
            data["context"] = json.loads(data["context"])
            if data["context"].get("lang"):
                del data["context"]["lang"]
            context.update(data["context"])

        ir_action = request.env["ir.actions.report"]
        action_py3o_report = ir_action.get_from_report_name(
            reportname, "py3o"
        ).with_context(**context)
        if not action_py3o_report:
            raise exceptions.HTTPException(
                description="Py3o action report not found for report_name "
                f"{reportname}"
            )
        res, filetype = ir_action._render(reportname, docids, data)
        filename = action_py3o_report.gen_report_download_filename(docids, data)
        if not filename.endswith(filetype):
            filename = f"{filename}.{filetype}"
        content_type = mimetypes.guess_type("x." + filetype)[0]
        http_headers = [
            ("Content-Type", content_type),
            ("Content-Length", len(res)),
            ("Content-Disposition", content_disposition(filename)),
        ]
        return request.make_response(res, headers=http_headers)

    @route()
    def report_download(self, data, context=None, token=None):
        """This function is used by 'qwebactionmanager.js' in order to trigger
        the download of a py3o/controller report.

        :param data: a javascript array JSON.stringified containg report
        internal url ([0]) and type [1]
        :returns: Response with a filetoken cookie and an attachment header
        """
        requestcontent = json.loads(data)
        url, report_type = requestcontent[0], requestcontent[1]
        if "py3o" not in report_type:
            return super().report_download(data, context=context, token=token)
        try:
            reportname = url.split("/report/py3o/")[1].split("?")[0]
            docids = None
            if "/" in reportname:
                reportname, docids = reportname.split("/")

            if docids:
                # Generic report:
                response = self.report_routes(
                    reportname, docids=docids, converter="py3o"
                )
            else:
                # Particular report:
                # decoding the args represented in JSON
                data = list(MultiDict(parse_qs(url.split("?")[1])).items())
                response = self.report_routes(
                    reportname, converter="py3o", **dict(data)
                )
            response.set_cookie("fileToken", context)
            return response
        except Exception as e:
            se = serialize_exception(e)
            error = {"code": 200, "message": "Odoo Server Error", "data": se}
            return request.make_response(html_escape(json.dumps(error)))
