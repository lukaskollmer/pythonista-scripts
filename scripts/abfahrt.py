#! python3

"""
abfahrt.py

TODO:
- make cells auto-update the time remaining
- swipe left to create reminders
- rewrite everithing using objc_util?
"""

import ui
import location
import requests
from datetime import datetime

endpoins = {
    'nearby_stations': 'https://www.mvg.de/fahrinfo/api/location/nearby',
    'departures': 'https://www.mvg.de/fahrinfo/api/departure/'
}
headers = {'X-MVG-Authorization-Key': '5af1beca494712ed38d313714d4caff6'}

def make_request(url, parameters):
    response = requests.get(url, headers=headers, params=parameters)
    return response.json()


def get_nearby_stations(location):
    params = {
        'latitude': location['latitude'],
        'longitude': location['longitude']
    }

    return make_request(endpoins['nearby_stations'], params)['locations']

def get_departures(station_id):
    url = endpoins['departures'] + str(station_id)

    return make_request(url, {'footway': 0})['departures']



class NearbyStationsViewController(ui.View):
    def __init__(self):
        self.tv = ui.TableView()
        self.tv.flex = 'WH'
        self.tv.data_source = self
        self.tv.delegate = self
        self.add_subview(self.tv)
        self.name = 'Nearby'
        self.right_button_items = [ui.ButtonItem(image=ui.Image.named('refresh'), title="refresh", action=lambda x: self.load_stations())]
        self.load_stations()

    def load_stations(self):
        self.stations = get_nearby_stations(location.get_location())
        self.tv.reload_data()

# Data Source
    def tableview_number_of_rows(self, tableview, section):
        return len(self.stations)

    def tableview_cell_for_row(self, tableview, section, row):
        station = self.stations[row]
        distance = station['distance']
        cell = ui.TableViewCell('value1')
        cell.text_label.text = station['name']
        cell.detail_text_label.text = f'{distance} m'
        return cell

# Delegate
    def tableview_did_select(self, tableview, section, row):
        #print(f'show upcoming departures for {self.stations[row]}')
        self.navigation_view.push_view(DeparturesViewController(self.stations[row]))


class DeparturesViewController(ui.View):
    def __init__(self, station):
        self.station = station
        self.departures = []

        self.tv = ui.TableView()
        self.tv.flex = "WH"
        self.tv.data_source = self
        self.tv.delegate = self # TODO use an objc delegate instead to spport custom swipe actions? (notifications!!!)
        self.add_subview(self.tv)

        self.load_departures()

    def load_departures(self):
        self.departures = get_departures(self.station['id'])
        self.tv.reload_data()


    def tableview_number_of_rows(self, tableview, section):
        return len(self.departures)

    def tableview_cell_for_row(self, tableview, section, row):
        departure = self.departures[row]
        product = departure['product']
        destination = departure['destination']
        label = departure['label']

        time_remaining = (datetime.fromtimestamp(departure['departureTime']/1000.0) - datetime.now()).total_seconds()
        if time_remaining > 60:
            time_remaining = f'{int(time_remaining / 60)} min'
        else:
            time_remaining = f'{int(time_remaining)} sec'

        cell = ui.TableViewCell('value1')
        cell.text_label.text = f'{label} - {destination}'
        cell.text_label.text_color = departure['lineBackgroundColor']
        cell.detail_text_label.text = time_remaining
        return cell



if __name__ == '__main__':
    #stations = get_nearby_stations(location.get_location())
    #for station in stations:
    #    print(station['name'])

    view = NearbyStationsViewController()
    nv = ui.NavigationView(view)
    nv.navigation_bar_hidden = False
    nv.present()
