import logging


def setup_system_wide_scheduler(app):
    # Import scheduler inside the function to avoid circular import
    from app.scheduler import scheduler
    from app.cronjobs.report_transactions import send_periodic_summary_for_all_users

    job_id = "system_wide_summary"

    # Check if the job already exists to avoid adding duplicate jobs
    if scheduler.get_job(job_id):
        logging.info(f"Job {job_id} already exists, skipping creation.")
        return

    # Schedule the job to run every 24 hours
    scheduler.add_job(
        func=send_periodic_summary_for_all_users,
        trigger="interval",
        days=1,  # Change this to 24 * 60 for once a day
        args=[app],  # Pass the app's current object
        id=job_id
    )
    logging.info(f"Job {job_id} has been added successfully.")
