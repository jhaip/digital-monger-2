import json
import gspread
import yaml
import datetime
from oauth2client.client import SignedJwtAssertionCredentials

json_key = json.load(open('Digital Monger Gspread access-896b64bbcb2d.json'))
scope = ['https://spreadsheets.google.com/feeds']
credentials = SignedJwtAssertionCredentials(json_key['client_email'],
	json_key['private_key'], scope)

gc = gspread.authorize(credentials)
    
config = yaml.load(open("config.yaml", 'r'))

def get_date_str(date):
    print date.strftime('%A %-m/%-d')
    return date.strftime('%A %-m/%-d')

def is_brother(s):
    if isinstance(s, basestring):
        s = s.replace("#fined","").replace("#done","").strip()
        if s in config['brothers']['nametoemail'].keys():
            return s
        elif s.lower() in config['brothers']['nicknametoname'].keys():
	    return config['brothers']['nicknametoname'][s.lower()]
    return None

def get_date_position(datestr):
    try:
    	c = wks.find(datestr)
    	return (c.row, c.col)
    except:
	raise Exception()

def get_shazam_rows(wks):
    shazam_rows = {}
    V = wks.col_values(1)
    for i, v in enumerate(V):
	if v is not None:
	    if v.strip() != "":
	        shazam_rows[i+1] = v  # +1 adjustment to 1-indexing
    return shazam_rows

def day_assignments(cell_values, description_row_map=None):
    assignments = []
    for i, v in enumerate(cell_values):
	v = is_brother(v)
	if v is not None:
	    if description_row_map is not None:
	    	assignments.append((v, description_row_map[i+1]))
	    else:
		assignments.append(v)
    return assignments

wks = gc.open("Shazams Spring 2015").sheet1
try:
    (dr, dc) = get_date_position(get_date_str(datetime.datetime(2015, 3, 12, 9, 6, 5)))
    description_row_map = get_shazam_rows(wks)
    print day_assignments(wks.col_values(dc), description_row_map)
except:
    print "didn't find date in shazams"

print "-"

wks = gc.open("PLP Dinner Duty Sign-ups - SP15").sheet1
try:
    (dr, dc) = get_date_position(get_date_str(datetime.datetime(2015, 4, 26, 9, 6, 5)))
    print day_assignments(wks.row_values(dr))
except:
    print "didn't find date in dinner duties"
