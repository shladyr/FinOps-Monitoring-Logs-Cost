#!/usr/bin/env python3
import argparse
import logging
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.logs_indexes_api import LogsIndexesApi
from webexteamssdk import WebexTeamsAPI


class DataDogLogsExclusionFilters:
    """
    Class for retrieving and printing exclusion filters for DataDog Logs Index.
    """
    def __init__(self, api_key, app_key, webex_token, room_id):
        """
        Initialize DataDogLogsExclusionFilters instance.

        Args:
            api_key (str): DataDog API key.
            app_key (str): DataDog App key.
        """
        self.api_key = api_key
        self.app_key = app_key
        self.api_client = self._create_api_client()
        self.webex_api = WebexTeamsAPI(access_token=webex_token)
        self.room_id = room_id

    def _create_api_client(self):
        """
        Create and configure the DataDog API client.

        Returns:
            ApiClient: Configured instance of the DataDog API client.
        """
        config = Configuration()
        config.api_key["apiKeyAuth"] = self.api_key
        config.api_key["appKeyAuth"] = self.app_key
        return ApiClient(configuration=config)

    def get_exclusion_filters(self, index_name):
        """
        Retrieve the exclusion filters for a specified Logs Index.

        Args:
            index_name (str): Name of the Logs Index.

        Returns:
            list: List of exclusion filters for the specified Logs Index.
        """
        logs_indexes_api = LogsIndexesApi(self.api_client)
        try:
            logs_index = logs_indexes_api.get_logs_index(index_name)
            exclusion_filters = logs_index.exclusion_filters
            return exclusion_filters
        except Exception as e:
            logging.error(f"Failed to retrieve exclusion filters: {str(e)}")
            return []

    def print_enabled_exclusion_filters(self, exclusion_filters):
        message = "Warning! DataDog Costs might be affected! Please check the List of enabled non-Prod Rules for Indexed Logs:\n"
        for i, exclusion_filter in enumerate(exclusion_filters, start=1):
            if getattr(exclusion_filter, "is_enabled", False):
                name = exclusion_filter.name
                if not any(pattern in name for pattern in ["Prod", "Stage", "Perf"]):
                    message += f"{i}. {name}\n"

        return message

    def send_to_webex_room(self, message):
        self.webex_api.messages.create(roomId=self.room_id, text=message)

    def send_print_output_to_webex_room(self):
        exclusion_filters = self.get_exclusion_filters("main")
        message = self.print_enabled_exclusion_filters(exclusion_filters)
        self.send_to_webex_room(message)



if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Retrieve exclusion filters for DataDog Logs Index.")
    parser.add_argument("--api-key", help="DataDog API key", required=True)
    parser.add_argument("--app-key", help="DataDog App key", required=True)
    parser.add_argument("--webex-token", help="Webex Teams API token", required=True)
    parser.add_argument("--room-id", help="Webex Teams Room ID", required=True)
    args = parser.parse_args()

    # Create an instance of DataDogLogsExclusionFilters
    datadog_logs_filters = DataDogLogsExclusionFilters(args.api_key, args.app_key, args.webex_token, args.room_id)

    # Send the print output to the Webex Room
    datadog_logs_filters.send_print_output_to_webex_room()


