from django.forms import ModelForm, Textarea
from auctions.models import Auction_listing, Bid



class ListingForm(ModelForm):
    class Meta:
        model = Auction_listing
        fields = ["title", "description", "starting_bid", "image_url", "category"]
        widgets = {
            "description" : Textarea(attrs={'cols':40, 'rows':6})
        }


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["offer"]
