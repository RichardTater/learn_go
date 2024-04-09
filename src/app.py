"""
AWS Worker Application

This module contains the handler function for an AWS worker. The handler function is responsible for processing and managing tasks related to AWS services. It utilizes the configured environment variables to interact with AWS resources.

Usage:
- Ensure that the required environment variables are configured in the '.env' file before running the application.
- The handler function processes incoming requests and performs the necessary actions based on the input.

For more information on the AWS Worker Application, please refer to the README.md file.
"""

import os
import sys
import logging

from lgcy_utils.aws.utilites.event_record import EventRecord

if "AWS_LAMBDA_FUNCTION_NAME" in os.environ:
    from src.helpers import imports  # add your imports here
else:
    from helpers import imports  # and here


def handler(event, context):
    TESTING = os.getenv("TESTING", "True").lower() == "true"
    logging.getLogger().setLevel(logging.INFO)
    logging.debug({"TESTING": TESTING})

    batch_item_failures = []
    for record in event["Records"]:
        logging.info("Record: {}".format(record))
        try:
            message = EventRecord.extract_message(record)
            process_message(message)
        except Exception as e:
            logging.exception("Exception on record while processing")
            batch_item_failures.append({"itemIdentifier": record["messageId"]})

    return {"batchItemFailures": batch_item_failures}


def process_message(message: dict):
    """
    Process a single message received from an SQS queue.

    Args:
        message (dict): A dictionary representing the message content.

    Description:
        Process a single record received from an SQS queue. Any code related
        to the processing of the message should be implemented within this
        function.

        If an error occurs during message processing, it should be raised to
        the caller for proper error handling. The caller (typically the
        handler function) will handle the error, including adding the message
        identifier to a list of failed messages (if necessary). This allows
        for proper handling and reporting of message processing failures,
        such as retrying the message or logging the failure for later
        analysis.
    """


if __name__ == "__main__":
    import json

    # Configure logging for local logs
    logging.basicConfig(
        level=logging.DEBUG, handlers=[logging.StreamHandler(sys.stdout)], force=True
    )

    with open("./src/event_record.json", "r") as event_record_json:
        event = json.load(event_record_json)

    # Replace Records with a message body to be ran locally while testing
    handler(event, None)
