import uuid
from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now
import logging
logger = logging.getLogger("django.request")

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.request_id = str(uuid.uuid4())

    def process_response(self, request, response):
        params = request.GET.dict() if request.method == "GET" else getattr(request, 'data', {})
        log_data = {
            "timestamp": now().isoformat(),
            "level": "INFO",
            "message": "",
            "endpoint": request.path,
            "request_id": getattr(request, "request_id", None),
            "parameters": params,
        }
        
        if isinstance(response.data, dict):
            if response.data.get('imported_rows'):
                log_data['imported_rows'] = response.data.get('imported_rows')
            if response.data.get('message'):
                log_data['message'] = response.data.get('message')
        
        logger.info(log_data)
        return response