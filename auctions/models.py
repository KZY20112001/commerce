from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    pass


class Auction_listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidded_listings")
    title = models.CharField(max_length=64, help_text="The title to be displayed")
    description = models.CharField(max_length=1000, blank = True, help_text="description of the item")
    starting_bid = models.DecimalField(max_digits=6,decimal_places=2, help_text = "Starting Bid Price")
    image_url = models.CharField(max_length = 2000, blank=True, help_text = "Optional Image URL link for the product")
    closed = models.BooleanField(default=False)
    category = models.CharField(max_length=64, blank= True, help_text = "Category of the item")
    watchlist_users = models.ManyToManyField(User, blank = True, related_name= "watchlist_listings")

    def current_price(self):
        return max([self.starting_bid] + [bid.offer for bid in self.bids.all()])

    def no_of_bids(self):
        return len(self.bids.all())

    def current_winner(self):
        if self.no_of_bids() > 0:
            return self.bids.get(offer=self.current_price())
        else:
            return None

    def __str__(self):
        return f"{self.title} by {self.owner}: {self.description}"



class Bid(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "bids_made")
    listing = models.ForeignKey(Auction_listing, on_delete = models.CASCADE, related_name ="bids")
    offer = models.DecimalField(max_digits=6,decimal_places=2, help_text = "How much are you willing to pay for this item?: ")

    def check_offer(self):
        #check if the offer is lower than the current price of the item
        if(self.offer <= self.listing.current_price()):
            raise ValidationError({'offer': _('Please make sure your offer is greater than the current price of the item.')})

    def __str__(self):
        return f"{self.user} has offered ${self.offer} for the item : {self.listing}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name ="comments")
    content = models.CharField(max_length = 2000)
    listing = models.ForeignKey(Auction_listing, on_delete = models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.user} commented on the item : {self.listing}.\n Comment : {self.comment}"
