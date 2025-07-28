from flask import Flask, request, jsonify
from smartbindb import SmartBinDB

# Flask অ্যাপ তৈরি
app = Flask(__name__)

# SmartBinDB ক্লাস ইন্সট্যান্স তৈরি
smartdb = SmartBinDB()

# BIN তথ্য অনুসন্ধান API Endpoint
@app.route("/bin_info", methods=["GET"])
def get_bin_info():
    bin_number = request.args.get("bin_number")
    if not bin_number:
        return jsonify({"error": "bin_number parameter is required"}), 400
    
    result = smartdb.get_bin_info(bin_number)
    
    if result.get("status") != "SUCCESS":
        return jsonify({"error": "BIN not found"}), 404
    
    return jsonify({"bin_info": result.get("data")})

# কান্ট্রি ভিত্তিক BIN অনুসন্ধান API Endpoint (রিসোর্স লিমিট দিয়ে)
@app.route("/bins_by_country", methods=["GET"])
def get_bins_by_country():
    country_code = request.args.get("country_code")
    if not country_code:
        return jsonify({"error": "country_code parameter is required"}), 400
    
    # ইউজারের চাওয়া পরিমাণ (লিমিট)
    limit = request.args.get("limit", 2000, type=int)
    
    # কান্ট্রি ভিত্তিক BIN অনুসন্ধান
    result = smartdb.get_bins_by_country(country_code, limit)
    
    if result.get("status") != "SUCCESS":
        return jsonify({"error": "No BINs found for the country"}), 404
    
    return jsonify({"country_results": result.get("data")})

# সকল কান্ট্রি ও তাদের BIN ডেটার পরিমাণ দেখানোর API Endpoint
@app.route("/country_list", methods=["GET"])
def get_country_list():
    # সকল দেশ ও তাদের BIN ডেটার পরিমাণ সম্পর্কে তথ্য পাওয়া
    countries_data = smartdb.get_all_countries_data()  # অনুমান করা হচ্ছে smartbindb লাইব্রেরিতে এই ফাংশন আছে
    country_info = []
    
    for country, data in countries_data.items():
        country_info.append({
            "country_name": country,
            "country_code": data.get("country_code"),
            "bins_count": len(data.get("bins", []))  # প্রতিটি দেশটির সাথে সম্পর্কিত BIN এর সংখ্যা
        })
    
    return jsonify({"countries": country_info})

# Flask অ্যাপ রান করা
if __name__ == "__main__":
    app.run(debug=True)
