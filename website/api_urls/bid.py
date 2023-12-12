from django.urls import path
from website.views import bid

urlpatterns = [
    path("create", bid.create_bid, name='create-bid'),
    path("getAll", bid.get_all_bids, name='get-all-bids'),
    path("getOne/<str:_id>", bid.get_one_bid, name='get-one-bid'),
    path("getAllByAuctionId/<int:auction_id>", bid.get_all_bids_by_auction_id,
         name='get-all-bids-by-auction-id'),
    path("getAllByBidderId/<int:bidder_id>", bid.get_all_bids_by_bidder_id,
         name='get-all-bids-by-bidder-id'),
    path("getAllByAuctionIdAndBidderId/<int:auction_id>/<int:bidder_id>",
         bid.get_all_bids_by_auction_id_and_bidder_id,
         name='get-all-bids-by-auction-id-and-bidder-id'),

    path("getWinnerByAuctionId/<int:auction_id>", bid.get_winner_by_auction_id,
         name='get-winner-by-auction-id'),
    path("updateOne/<str:_id>", bid.update_one_bid, name='update-one-bid'),
    path("deleteOne/<str:_id>", bid.delete_one_bid, name='delete-one-bid'),
    path("deleteAllByAuctionId/<int:auction_id>",
         bid.delete_all_bids_by_auction_id,
         name='delete-all-bids-by-auction-id'),
]
