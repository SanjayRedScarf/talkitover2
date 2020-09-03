from flask import request

class GoogleAdsService:
    def get_google_ads_data_from_url(self): 
        campaign = request.args.get('campaign')
        group = request.args.get('group')
        geo = request.args.get('geo')
        device = request.args.get('device')

        google_ads_data_dictionary = {
            "campaign": campaign,
            "group": group,
            "geo": geo,
            "device": device
        }

        return google_ads_data_dictionary