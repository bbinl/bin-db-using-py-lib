# SmartBin API

This API allows you to access BIN information, search BINs by country, and get a list of countries with the number of BINs available.

## Endpoints

1. **/bin_info** - Retrieve information about a specific BIN number.
   - **GET** `/bin_info?bin_number={bin_number}`
   - Example: `/bin_info?bin_number=123456`

2. **/bins_by_country** - Retrieve BINs by country with a limit.
   - **GET** `/bins_by_country?country_code={country_code}&limit={limit}`
   - Example: `/bins_by_country?country_code=BD&limit=100`

3. **/country_list** - Get a list of countries with the number of BINs available in each.
   - **GET** `/country_list`
   - Example: `/country_list`

## Deployment

To deploy this API on Vercel:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
