from model import EventListDao


class EventListService:
    """

    """
    def __init__(self):
        self.event_list_dao = EventListDao()

    def event_banner_list_logic(self, connection, data):
        """

        Args:
            connection:
            data:

        Returns:

        """

        if data['is_proceeding']:
            event_list = self.event_list_dao.get_proceeding_event_banner_list(connection, data)
        else:
            event_list = self.event_list_dao.get_closed_event_banner_list(connection, data)
        return event_list

    def event_detail_information_logic(self, connection, event_id):
        """

        Args:
            connection:
            event_id:

        Returns:

        """

        event_info = self.event_list_dao.get_event_information(connection, event_id)
        return event_info

    def event_detail_button_list_logic(self, connection, event_id):
        """

        Args:
            connection:
            event_id:

        Returns:

        """

        event_button_list = self.event_list_dao.get_event_button(connection,event_id)
        return event_button_list

    def event_detail_list_logic(self, connection, data):
        """

        Args:
            connection:
            data:

        Returns:

        """

        is_button = self.event_list_dao.is_event_has_button(connection, data['event_id'])

        if is_button:
            event_button_products = self.event_list_dao.get_event_button_product_list(connection, data)
            return event_button_products
        else:
            event_products = self.event_list_dao.get_event_product_list(connection, data)
            return event_products
