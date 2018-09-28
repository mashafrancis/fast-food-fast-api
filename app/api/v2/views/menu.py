from flask import request, Blueprint
from flask.views import MethodView

import app.api.common.responses as MenuError

from app.api.v2.models.menu import Menu
from app.api.common.responses import Response

menu = Blueprint('menu', __name__)


class MenuView(MethodView):
    """Contains GET and POST methods"""

    def post(self):
        """Endpoint for adding a new order."""
        data = request.get_json(force=True)
        name = data['name']
        description = data['description']

        try:
            Menu.validate_menu_details(name, description)
            menu_name = Menu.find_by_name(name)
            if not menu_name:
                new_menu = Menu(name=name,
                                description=description)
                new_menu.save()
                return Response.create_resource('A new menu has been added successfully.')
            raise MenuError.Conflict('The menu name already exists. Should you update?')

        except MenuError.Conflict as e:
            return e.message
        except MenuError.BadRequest as e:
            return e.message

    def get(self):
        """Endpoint for fetching all orders."""
        results = []
        all_menu = Menu.list_all_menu()
        try:
            if all_menu:
                for _menu in all_menu:
                    obj = Response.define_menu(_menu)
                    results.append(obj)
                return Response.complete_request(results)
            else:
                raise MenuError.NotFound('Sorry, No Category found! Create one.')
        except MenuError.NotFound as e:
            return e.message


# Define API resource
menu_view = MenuView.as_view('menu_view')

menu.add_url_rule('menu',
                  view_func=menu_view,
                  methods=['POST', 'GET', 'DELETE'])