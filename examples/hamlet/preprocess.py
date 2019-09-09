"""
A script to download the humlet dataset and apply some preprocesses on it
"""

import os
import sys
import zipfile

from argparse import ArgumentParser
from pyspark.sql import SparkSession
from urllib.request import urlretrieve

def check_if_dataset_exists():
    data_name = 'RealWorldDatasets'
    if not os.path.isdir('./dataset/%s' % data_name):
        print("Downloading '%s' and saving it in ./dataset" % data_name)
        url = 'http://cseweb.ucsd.edu/~arunkk/hamlet/%s.zip' % data_name
        savePath = './dataset/%s.zip' % data_name
        urlretrieve(url, savePath)
        with zipfile.ZipFile(savePath) as zip:
            zip.extractall(path='./dataset')

if __name__ == "__main__":
    # Parses command-line arguments
    parser = ArgumentParser()
    parser.add_argument('--data', dest='data', help='walmart, expedia, flights, yelp, moivelens1m, lastfm, or bookcrossing', type=str, required=True)
    parser.add_argument('--sample_ratio', dest='sample_ratio', help='Sample Ratio', type=float, default=1.0)
    args = parser.parse_args()

    # Checks if the dataset exists
    check_if_dataset_exists()

    spark = SparkSession.builder.appName('preprocess').getOrCreate()
    base_path = './dataset/RealWorldDatasets/'

    if args.data == 'walmart':
        # Loads the Walmart data whose join graph is as follows;
        #                                                        _ R2_stores{store, ...}
        #                                                       /
        #  S_sales{weekly_sales, sid, dept, ..., purchaseid, store}
        #                                            /
        #           R1_indicators{purchaseid, ...} _/
        #
        spark.read.option('header', True).option('inferSchema', True).csv(base_path + 'WalMart/S_sales.csv').createOrReplaceTempView('S_sales')
        spark.read.option('header', True).option('inferSchema', True).csv(base_path + 'WalMart/R1_indicators.csv').createOrReplaceTempView('R1_indicators')
        spark.read.option('header', True).option('inferSchema', True).csv(base_path + 'WalMart/R2_stores.csv').createOrReplaceTempView('R2_stores')
        sdf = spark.sql(
            "SELECT " \
                "(CAST(TRIM(BOTH '\\'' FROM weekly_sales) AS INT) - 1) weekly_sales, " \
                "CAST(TRIM(BOTH '\\'' FROM sid) AS INT) sid, " \
                "CAST(TRIM(BOTH '\\'' FROM dept) AS INT) dept, " \
                "CAST(TRIM(BOTH '\\'' FROM s.store) AS INT) store, " \
                "CAST(TRIM(BOTH '\\'' FROM type) AS INT) type, " \
                "size, " \
                "temperature_stdev, " \
                "fuel_price_avg, " \
                "fuel_price_stdev, " \
                "cpi_avg, " \
                "cpi_stdev, " \
                "unemployment_avg, " \
                "unemployment_stdev, " \
                "holidayfreq " \
            "FROM " \
                "S_sales s, " \
                "R1_indicators i, " \
                "R2_stores st " \
            "WHERE " \
                "s.purchaseid = i.purchaseid AND " \
                "s.store = st.store")

    elif args.data == 'yelp':
        spark.read.option('header', True).option('inferSchema', True).csv(base_path + 'Yelp/S_ratings.csv').createOrReplaceTempView('S_ratings')
        spark.read.option('header', True).option('inferSchema', True).csv(base_path + 'Yelp/R1_businesses.csv').createOrReplaceTempView('R1_businesses')
        spark.read.option('header', True).option('inferSchema', True).csv(base_path + 'Yelp/R2_users.csv').createOrReplaceTempView('R2_users')
        sdf = spark.sql(
            "SELECT " \
                "CAST(TRIM(BOTH '\\'' FROM stars) AS INT) stars, " \
                "hash(r.userid) userid, " \
                "hash(reviewid) reviewid, " \
                "hash(r.businessid) businessid, " \
                "hash(cat109) cat109, " \
                "hash(cat363) cat363, " \
                "hash(cat361) cat361, " \
                "hash(cat366) cat366, " \
                "hash(cat344) cat344, " \
                "hash(cat33) cat33, " \
                "hash(city) city, " \
                "hash(cat501) cat501, " \
                "hash(cat444) cat444, " \
                "hash(cat404) cat404, " \
                "hash(cat259) cat259, " \
                "hash(cat246) cat246, " \
                "hash(cat79) cat79, " \
                "hash(open) open, " \
                "hash(cat221) cat221, " \
                "hash(cat314) cat314, " \
                "hash(cat104) cat104, " \
                "hash(state) state, " \
                "hash(latitude) latitude, " \
                "hash(longitude) longitude, " \
                "hash(bstars) bstars, " \
                "breviewcnt, " \
                "wday1, " \
                "wday2, " \
                "wday3, " \
                "wday4, " \
                "wday5, " \
                "wend1, " \
                "wend2, " \
                "wend3, " \
                "wend4, " \
                "wend5, " \
                "ureviewcnt, " \
                "ustars, " \
                "hash(vuseful) vuseful, " \
                "hash(vfunny) vfunny, " \
                "hash(vcool) vcool, " \
                "hash(gender) gender " \
            "FROM " \
                "S_ratings r, " \
                "R1_businesses b, " \
                "R2_users u " \
            "WHERE " \
                "r.businessid = b.businessid AND " \
                "r.userid = u.userid")

    elif args.data == 'flights':
        spark.read.option('header', True).option('inferSchema', True).csv(base_path + 'Flights/S_routes.csv').createOrReplaceTempView('S_routes')
        spark.read.option('header', True).option('inferSchema', True).csv(base_path + 'Flights/R1_airlines.csv').createOrReplaceTempView('R1_airlines')
        spark.read.option('header', True).option('inferSchema', True).csv(base_path + 'Flights/R2_sairports.csv').createOrReplaceTempView('R2_sairports')
        spark.read.option('header', True).option('inferSchema', True).csv(base_path + 'Flights/R3_dairports.csv').createOrReplaceTempView('R3_dairports')
        sdf = spark.sql(
            "SELECT " \
                "CAST(codeshare AS BOOLEAN) codeshare, " \
                "hash(r.airlineid) airlineid, " \
                "hash(r.sairportid) sairportid, " \
                "hash(r.dairportid) dairportid, " \
                "hash(scity) scity, " \
                "hash(dcity) dcity, " \
                "hash(acountry) acountry, " \
                "hash(dcountry) dcountry, " \
                "hash(scountry) scountry, " \
                "hash(ddst) ddst, " \
                "hash(sdst) sdst, " \
                "stimezone, " \
                "dtimezone, " \
                "dlongitude, " \
                "slongitude, " \
                "hash(eq8) eq8, " \
                "hash(eq17) eq17, " \
                "hash(eq22) eq22, " \
                "name1, " \
                "hash(eq2) eq2, " \
                "hash(eq1) eq1, " \
                "hash(eq19) eq19, " \
                "hash(eq20) eq20, " \
                "hash(eq28) eq28, " \
                "slatitude, " \
                "dlatitude, " \
                "hash(eq46) eq46, " \
                "hash(name4) name4, " \
                "hash(active) active, " \
                "hash(eq3) eq3, " \
                "hash(eq71) eq71, " \
                "hash(eq25) eq25, " \
                "hash(eq30) eq30, " \
                "hash(eq4) eq4, " \
                "hash(eq45) eq45, " \
                "hash(eq14) eq14, " \
                "hash(eq12) eq12, " \
                "hash(name2) name2, " \
                "hash(eq15) eq15, " \
                "hash(eq31) eq31, " \
                "hash(eq5) eq5 " \
            "FROM " \
                "S_routes r, " \
                "R1_airlines a, " \
                "R2_sairports s, " \
                "R3_dairports d " \
            "WHERE " \
                "r.airlineid = a.airlineid AND " \
                "r.sairportid = s.sairportid AND " \
                "r.dairportid = d.dairportid")

    elif args.data == 'expedia':
        spark.read.option('header', True).option('inferSchema', True).csv(base_path + 'Expedia/S_listings.csv').createOrReplaceTempView('S_listings')
        spark.read.option('header', True).option('inferSchema', True).csv(base_path + 'Expedia/R1_hotels.csv').createOrReplaceTempView('R1_hotels')
        spark.read.option('header', True).option('inferSchema', True).csv(base_path + 'Expedia/R2_searches.csv').createOrReplaceTempView('R2_searches')
        sdf = spark.sql(
            "SELECT " \
                "CAST(TRIM(BOTH '\\'' FROM position) AS INT) position, " \
                "hash(l.srch_id) srch_id, " \
                "hash(l.prop_id) prop_id, " \
                "hash(prop_location_score1) prop_location_score1, " \
                "hash(prop_location_score2) prop_location_score2, " \
                "hash(prop_log_historical_price) prop_log_historical_price, " \
                "hash(price_usd) price_usd, " \
                "hash(promotion_flag) promotion_flag, " \
                "hash(orig_destination_distance) orig_destination_distance, " \
                "hash(prop_country_id) prop_country_id, " \
                "hash(prop_starrating) prop_starrating, " \
                "hash(prop_review_score) prop_review_score, " \
                "hash(prop_brand_bool) prop_brand_bool, " \
                "hash(count_clicks) count_clicks, " \
                "hash(avg_bookings_usd) avg_bookings_usd, " \
                "hash(stdev_bookings_usd) stdev_bookings_usd, " \
                "hash(count_bookings) count_bookings, " \
                "hash(year) year, " \
                "hash(month) month, " \
                "hash(weekofyear) weekofyear, " \
                "hash(time) time, " \
                "hash(site_id) site_id, " \
                "hash(visitor_location_country_id) visitor_location_country_id, " \
                "hash(srch_destination_id) srch_destination_id, " \
                "hash(srch_length_of_stay) srch_length_of_stay, " \
                "hash(srch_booking_window) srch_booking_window, " \
                "hash(srch_adults_count) srch_adults_count, " \
                "hash(srch_children_count) srch_children_count, " \
                "hash(srch_room_count) srch_room_count, " \
                "hash(srch_saturday_night_bool) srch_saturday_night_bool, " \
                "hash(random_bool) random_bool " \
            "FROM " \
                "S_listings l, " \
                "R1_hotels h, " \
                "R2_searches s " \
            "WHERE " \
                "l.srch_id = s.srch_id AND " \
                "l.prop_id = h.prop_id")

    elif args.data == 'movielens':
        spark.read.option('header', True).option('inferSchema', True).csv(base_path + 'Movies/S_ratings.csv').createOrReplaceTempView('S_ratings')
        spark.read.option('header', True).option('inferSchema', True).csv(base_path + 'Movies/R1_users.csv').createOrReplaceTempView('R1_users')
        spark.read.option('header', True).option('inferSchema', True).csv(base_path + 'Movies/R2_movies.csv').createOrReplaceTempView('R2_movies')
        sdf = spark.sql(
            "SELECT " \
                "CAST(TRIM(BOTH '\\'' FROM rating) AS INT) rating, " \
                "hash(r.movieid) movieid, " \
                "hash(r.userid) userid, " \
                "hash(gender) gender, " \
                "hash(age) age, " \
                "hash(occupation) occupation, " \
                "hash(zipcode) zipcode, " \
                "hash(namewords) namewords, " \
                "hash(namepar) namepar, " \
                "hash(year) year, " \
                "hash(action) action, " \
                "hash(adventure) adventure, " \
                "hash(animation) animation, " \
                "hash(`children.s`) childrens, " \
                "hash(comedy) comedy, " \
                "hash(crime) crime, " \
                "hash(documentary) documentary, " \
                "hash(drama) drama, " \
                "hash(fantasy) fantasy, " \
                "hash(`film.noir`) filmnoir, " \
                "hash(horror) horror, " \
                "hash(musical) musical, " \
                "hash(mystery) mystery, " \
                "hash(romance) romance, " \
                "hash(`sci.fi`) scifi, " \
                "hash(thriller) thriller, " \
                "hash(war) war, " \
                "hash(western) western " \
            "FROM " \
                "S_ratings r, " \
                "R1_users u, " \
                "R2_movies m " \
            "WHERE " \
                "r.userid = u.userid AND " \
                "r.movieid = m.movieid")

    elif args.data == 'lastfm':
        spark.read.option('header', True).option('inferSchema', True).csv(base_path + 'LastFM/S_plays.csv').createOrReplaceTempView('S_plays')
        spark.read.option('header', True).option('inferSchema', True).csv(base_path + 'LastFM/R1_artists.csv').createOrReplaceTempView('R1_artists')
        spark.read.option('header', True).option('inferSchema', True).csv(base_path + 'LastFM/R2_users.csv').createOrReplaceTempView('R2_users')
        sdf = spark.sql(
            "SELECT " \
                "CAST(TRIM(BOTH '\\'' FROM plays) AS INT) plays, " \
                "hash(p.userid) userid, " \
                "hash(p.artistid) artistid, " \
                "hash(numscrobbles) numscrobbles, " \
                "hash(numlistens) numlistens, " \
                "hash(rock) rock, " \
                "hash(electronic) electronic, " \
                "hash(indie) indie, " \
                "hash(pop) pop, " \
                "hash(hiphop) hiphop, " \
                "hash(gender) gender, " \
                "hash(age) age, " \
                "hash(country) country, " \
                "hash(year) year " \
            "FROM " \
                "S_plays p, " \
                "R1_artists a, " \
                "R2_users u " \
            "WHERE " \
                "p.artistid = a.artistid AND " \
                "p.userid = u.userid")

    elif args.data == 'books':
        spark.read.option('header', True).option('inferSchema', True).csv(base_path + 'Books/S_ratings.csv').createOrReplaceTempView('S_ratings')
        spark.read.option('header', True).option('inferSchema', True).csv(base_path + 'Books/R1_users.csv').createOrReplaceTempView('R1_users')
        spark.read.option('header', True).option('inferSchema', True).csv(base_path + 'Books/R2_books.csv').createOrReplaceTempView('R2_books')
        sdf = spark.sql(
            "SELECT " \
                "CAST(TRIM(BOTH '\\'' FROM rating) AS INT) rating, " \
                "hash(r.userid) userid, " \
                "hash(r.bookid) bookid, " \
                "hash(titlewords) titlewords, " \
                "hash(authorwords) authorwords, " \
                "hash(year) year, " \
                "hash(publisher) publisher, " \
                "hash(country) country, " \
                "hash(age) age " \
            "FROM " \
                "S_ratings r, " \
                "R1_users u, " \
                "R2_books b " \
            "WHERE " \
                "r.userid = u.userid AND " \
                "r.bookid = b.bookid")

    else:
        print('Unknown data:%s' % args.data)
        sys.exit(-1)

    # Samples a part of the dataset then outputs it as the parquet format
    df = sdf.sample(args.sample_ratio).toPandas()
    df.to_parquet('%s.parquet' % args.data)

