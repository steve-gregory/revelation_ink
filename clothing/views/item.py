"""
Revelation Ink Clothing Item models
"""

from djangorestframework.reverse import reverse
from djangorestframework.views import View
from djangorestframework.response import Response
from djangorestframework import status

from revelation_ink.logger import logger

from clothing.models import Item as ItemModel

class ItemManager(View):
    """
    Represents:
        A Manager of Item
        Calls to the Item Class
    """
    def get(self, request):
        """
        List all items that match USER
        """
        items = ItemModel.objects.all()
        return [i.json() for i in items]
    def post(self, request):
        """
        Create a new item with POST credentials
        TODO: Determine if this will ever be used
        """
	post_params = dict(request.DATA.items())
        return post_params

class Item(View):
    """
    Represents:
        Calls to modify the single Item
    """
    def get(self, request, item_id):
        """
        Return the item inofrmation
        TODO: A list of valid endpoints ?
        """
        item = ItemModel.objects.get(id=item_id)
        return item.json()
    def put(self, request, item_id):
        """
        Update information for the item (Meta-Information only?)
        """
        item = ItemModel.objects.get(id=item_id)
	#put_params = dict(request.DATA.items())
        #update values
        #save model
        return item.json()

