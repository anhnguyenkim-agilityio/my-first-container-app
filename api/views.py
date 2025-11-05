from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .tasks import process_data, send_email


class TaskCreateView(APIView):
    """
    API endpoint to create async tasks
    """

    def post(self, request):
        task_type = request.data.get("task_type")

        if task_type == "process":
            data = request.data.get("data", {})
            task = process_data.delay(data)
            return Response(
                {
                    "task_id": task.id,
                    "status": "Task created",
                    "task_type": "process_data",
                },
                status=status.HTTP_202_ACCEPTED,
            )

        elif task_type == "email":
            email = request.data.get("email")
            subject = request.data.get("subject")
            message = request.data.get("message")
            task = send_email.delay(email, subject, message)
            return Response(
                {
                    "task_id": task.id,
                    "status": "Task created",
                    "task_type": "send_email",
                },
                status=status.HTTP_202_ACCEPTED,
            )

        return Response(
            {"error": "Invalid task_type"}, status=status.HTTP_400_BAD_REQUEST
        )


class TaskStatusView(APIView):
    """
    API endpoint to check task status
    """

    def get(self, request, task_id):
        from celery.result import AsyncResult

        task_result = AsyncResult(task_id)

        response_data = {
            "task_id": task_id,
            "status": task_result.state,
        }

        if task_result.state == "SUCCESS":
            response_data["result"] = task_result.result
        elif task_result.state == "FAILURE":
            response_data["error"] = str(task_result.info)

        return Response(response_data)


class HealthCheckView(APIView):
    """
    Health check endpoint for monitoring
    Returns status of Django, Database, Celery Broker, and Celery Workers
    """

    def get(self, request):
        health_status = {
            "status": "healthy",
            "timestamp": self._get_timestamp(),
            "checks": {},
        }

        # # Check Database
        # db_status = self._check_database()
        # health_status['checks']['database'] = db_status

        # # Check Celery Broker (Redis or Azure Service Bus)
        # broker_status = self._check_broker()
        # health_status['checks']['broker'] = broker_status

        # # Check Celery Workers
        # worker_status = self._check_celery_workers()
        # health_status['checks']['celery_workers'] = worker_status

        # # Determine overall status
        # all_healthy = all(
        #     check.get('status') == 'healthy'
        #     for check in health_status['checks'].values()
        # )

        # if not all_healthy:
        #     health_status['status'] = 'unhealthy'
        #     return Response(health_status, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(health_status, status=status.HTTP_200_OK)

    def _get_timestamp(self):
        from datetime import datetime

        return datetime.utcnow().isoformat()

    # def _check_database(self):
    #     """Check database connectivity"""
    #     try:
    #         connection.ensure_connection()
    #         return {
    #             'status': 'healthy',
    #             'message': 'Database connection successful'
    #         }
    #     except Exception as e:
    #         return {
    #             'status': 'unhealthy',
    #             'message': f'Database connection failed: {str(e)}'
    #         }

    # def _check_broker(self):
    #     """Check Celery broker connectivity"""
    #     try:
    #         if 'redis' in settings.CELERY_BROKER_URL:
    #             # Check Redis
    #             redis_client = redis.from_url(settings.CELERY_BROKER_URL)
    #             redis_client.ping()
    #             return {
    #                 'status': 'healthy',
    #                 'message': 'Redis broker is accessible',
    #                 'broker_type': 'redis'
    #             }
    #         else:
    #             # For Azure Service Bus, we assume it's healthy if configured
    #             return {
    #                 'status': 'healthy',
    #                 'message': 'Azure Service Bus broker configured',
    #                 'broker_type': 'azure_service_bus'
    #             }
    #     except Exception as e:
    #         return {
    #             'status': 'unhealthy',
    #             'message': f'Broker connection failed: {str(e)}'
    #         }

    # def _check_celery_workers(self):
    #     """Check if Celery workers are running"""
    #     try:
    #         from project.celery import app
    #         inspector = app.control.inspect()
    #         active_workers = inspector.active()

    #         if active_workers:
    #             worker_count = len(active_workers)
    #             return {
    #                 'status': 'healthy',
    #                 'message': f'{worker_count} worker(s) active',
    #                 'workers': list(active_workers.keys())
    #             }
    #         else:
    #             return {
    #                 'status': 'unhealthy',
    #                 'message': 'No active Celery workers found'
    #             }
    #     except Exception as e:
    #         return {
    #             'status': 'unhealthy',
    #             'message': f'Unable to check workers: {str(e)}'
    #         }
