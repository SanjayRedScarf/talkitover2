from flask import request
from models import google_ads_data

class GoogleAdsService:
    def get_google_ads_data_from_url(self): 

        """
        Gets the parameters from the URL passed from Google Ads.  These parameters are then hidden from user view via JavaScript.
        """
        
        campaign = ""
        group = ""
        geo = ""
        device = ""
        
        campaign = request.args.get('campaign')
        group = request.args.get('group')
        geo = request.args.get('geo')
        device = request.args.get('device')

        return google_ads_data.GoogleAdsData(campaign, group, geo, device)