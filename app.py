import webbrowser
from quart import Quart, request, jsonify, render_template
from smartbindb import SmartBinDB

# Quart অ্যাপ তৈরি
app = Quart(__name__)

# SmartBinDB ক্লাস ইন্সট্যান্স তৈরি
smartdb = SmartBinDB()

# ইনডেক্স পেইজ (Documentation) এর জন্য রুট
@app.route("/", methods=["GET"])
async def index():
    return await render_template("index.html")

# BIN তথ্য অনুসন্ধান API Endpoint
@app.route("/bin_info", methods=["GET"])
async def get_bin_info():
    bin_number = request.args.get("bin_number")
    if not bin_number:
        return jsonify({"error": "bin_number parameter is required"}), 400

    result = await smartdb.get_bin_info(bin_number)  # অ্যাসিঙ্ক্রোনাস ফাংশন কল

    if result.get("status") != "SUCCESS":
        return jsonify({"error": "BIN not found"}), 404

    return jsonify({"bin_info": result.get("data")})

# কান্ট্রি ভিত্তিক BIN অনুসন্ধান API Endpoint (রিসোর্স লিমিট দিয়ে)
@app.route("/bins_by_country", methods=["GET"])
async def get_bins_by_country():
    country_code = request.args.get("country_code")
    if not country_code:
        return jsonify({"error": "country_code parameter is required"}), 400

    limit = request.args.get("limit", 2000, type=int)

    result = await smartdb.get_bins_by_country(country_code, limit)  # অ্যাসিঙ্ক্রোনাস ফাংশন কল

    if result.get("status") != "SUCCESS":
        return jsonify({"error": "No BINs found for the country"}), 404

    return jsonify({"country_results": result.get("data")})

# Flask অ্যাপ রান করার জন্য
if __name__ == "__main__":
    # পোর্ট সেট করে Flask অ্যাপ রান করা
    port = 5000
    app.run(debug=True, host="0.0.0.0", port=port)

    # Flask অ্যাপ চালানোর পরে ইনডেক্স পেইজ অটোমেটিক্যালি ওপেন করা
    webbrowser.open(f'http://127.0.0.1:{port}/')
