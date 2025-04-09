import os
import maxminddb
import ipaddress
from collections import defaultdict

country_list = [
    {"acronym": "Unknown", "name": "Unknown"},
    {"acronym": "A1", "name": "Anonymous Proxy"},
    {"acronym": "A2", "name": "Satellite Provider"},
    {"acronym": "AD", "name": "Andorra"},
    {"acronym": "AE", "name": "United Arab Emirates"},
    {"acronym": "AF", "name": "Afghanistan"},
    {"acronym": "AG", "name": "Antigua and Barbuda"},
    {"acronym": "AI", "name": "Anguilla"},
    {"acronym": "AL", "name": "Albania"},
    {"acronym": "AM", "name": "Armenia"},
    {"acronym": "AN", "name": "Netherlands Antilles"},
    {"acronym": "AO", "name": "Angola"},
    {"acronym": "AP", "name": "Asia/Pacific Region"},
    {"acronym": "AQ", "name": "Antarctica"},
    {"acronym": "AR", "name": "Argentina"},
    {"acronym": "AS", "name": "American Samoa"},
    {"acronym": "AT", "name": "Austria"},
    {"acronym": "AU", "name": "Australia"},
    {"acronym": "AW", "name": "Aruba"},
    {"acronym": "AX", "name": "Aland Islands"},
    {"acronym": "AZ", "name": "Azerbaijan"},
    {"acronym": "BA", "name": "Bosnia and Herzegovina"},
    {"acronym": "BB", "name": "Barbados"},
    {"acronym": "BD", "name": "Bangladesh"},
    {"acronym": "BE", "name": "Belgium"},
    {"acronym": "BF", "name": "Burkina Faso"},
    {"acronym": "BG", "name": "Bulgaria"},
    {"acronym": "BH", "name": "Bahrain"},
    {"acronym": "BI", "name": "Burundi"},
    {"acronym": "BJ", "name": "Benin"},
    {"acronym": "BL", "name": "Saint Barthelemy"},
    {"acronym": "BM", "name": "Bermuda"},
    {"acronym": "BN", "name": "Brunei"},
    {"acronym": "BO", "name": "Bolivia"},
    {"acronym": "BQ", "name": "Caribbean Netherlands"},
    {"acronym": "BR", "name": "Brazil"},
    {"acronym": "BS", "name": "Bahamas"},
    {"acronym": "BT", "name": "Bhutan"},
    {"acronym": "BV", "name": "Bouvet Island"},
    {"acronym": "BW", "name": "Botswana"},
    {"acronym": "BY", "name": "Belarus"},
    {"acronym": "BZ", "name": "Belize"},
    {"acronym": "CA", "name": "Canada"},
    {"acronym": "CC", "name": "Cocos (Keeling) Islands"},
    {"acronym": "CD", "name": "The Democratic Republic of the Congo"},
    {"acronym": "CF", "name": "Central African Republic"},
    {"acronym": "CG", "name": "Congo"},
    {"acronym": "CH", "name": "Switzerland"},
    {"acronym": "CI", "name": "Cote D'Ivoire"},
    {"acronym": "CK", "name": "Cook Islands"},
    {"acronym": "CL", "name": "Chile"},
    {"acronym": "CM", "name": "Cameroon"},
    {"acronym": "CN", "name": "China"},
    {"acronym": "CO", "name": "Colombia"},
    {"acronym": "CR", "name": "Costa Rica"},
    {"acronym": "CU", "name": "Cuba"},
    {"acronym": "CV", "name": "Cabo Verde"},
    {"acronym": "CW", "name": "Curaçao"},
    {"acronym": "CX", "name": "Christmas Island"},
    {"acronym": "CY", "name": "Cyprus"},
    {"acronym": "CZ", "name": "Czechia"},
    {"acronym": "DE", "name": "Germany"},
    {"acronym": "DJ", "name": "Djibouti"},
    {"acronym": "DK", "name": "Denmark"},
    {"acronym": "DM", "name": "Dominica"},
    {"acronym": "DO", "name": "Dominican Republic"},
    {"acronym": "DZ", "name": "Algeria"},
    {"acronym": "EC", "name": "Ecuador"},
    {"acronym": "EE", "name": "Estonia"},
    {"acronym": "EG", "name": "Egypt"},
    {"acronym": "EH", "name": "Western Sahara"},
    {"acronym": "ER", "name": "Eritrea"},
    {"acronym": "ES", "name": "Spain"},
    {"acronym": "ET", "name": "Ethiopia"},
    {"acronym": "EU", "name": "Europe"},
    {"acronym": "FI", "name": "Finland"},
    {"acronym": "FJ", "name": "Fiji"},
    {"acronym": "FK", "name": "Falkland Islands (Malvinas)"},
    {"acronym": "FM", "name": "Federated States of Micronesia"},
    {"acronym": "FO", "name": "Faroe Islands"},
    {"acronym": "FR", "name": "France"},
    {"acronym": "FX", "name": "France, Metropolitan"},
    {"acronym": "GA", "name": "Gabon"},
    {"acronym": "GB", "name": "United Kingdom"},
    {"acronym": "GD", "name": "Grenada"},
    {"acronym": "GE", "name": "Georgia"},
    {"acronym": "GF", "name": "French Guiana"},
    {"acronym": "GG", "name": "Guernsey"},
    {"acronym": "GH", "name": "Ghana"},
    {"acronym": "GI", "name": "Gibraltar"},
    {"acronym": "GL", "name": "Greenland"},
    {"acronym": "GM", "name": "Gambia"},
    {"acronym": "GN", "name": "Guinea"},
    {"acronym": "GP", "name": "Guadeloupe"},
    {"acronym": "GQ", "name": "Equatorial Guinea"},
    {"acronym": "GR", "name": "Greece"},
    {"acronym": "GS", "name": "South Georgia and the South Sandwich Islands"},
    {"acronym": "GT", "name": "Guatemala"},
    {"acronym": "GU", "name": "Guam"},
    {"acronym": "GW", "name": "Guinea-Bissau"},
    {"acronym": "GY", "name": "Guyana"},
    {"acronym": "HK", "name": "Hong Kong"},
    {"acronym": "HM", "name": "Heard Island and McDonald Islands"},
    {"acronym": "HN", "name": "Honduras"},
    {"acronym": "HR", "name": "Croatia"},
    {"acronym": "HT", "name": "Haiti"},
    {"acronym": "HU", "name": "Hungary"},
    {"acronym": "ID", "name": "Indonesia"},
    {"acronym": "IE", "name": "Ireland"},
    {"acronym": "IL", "name": "Israel"},
    {"acronym": "IM", "name": "Isle of Man"},
    {"acronym": "IN", "name": "India"},
    {"acronym": "IO", "name": "British Indian Ocean Territory"},
    {"acronym": "IQ", "name": "Iraq"},
    {"acronym": "IR", "name": "Islamic Republic of Iran"},
    {"acronym": "IS", "name": "Iceland"},
    {"acronym": "IT", "name": "Italy"},
    {"acronym": "JE", "name": "Jersey"},
    {"acronym": "JM", "name": "Jamaica"},
    {"acronym": "JO", "name": "Jordan"},
    {"acronym": "JP", "name": "Japan"},
    {"acronym": "KE", "name": "Kenya"},
    {"acronym": "KG", "name": "Kyrgyzstan"},
    {"acronym": "KH", "name": "Cambodia"},
    {"acronym": "KI", "name": "Kiribati"},
    {"acronym": "KM", "name": "Comoros"},
    {"acronym": "KN", "name": "Saint Kitts and Nevis"},
    {"acronym": "KP", "name": "Democratic People's Republic of Korea"},
    {"acronym": "KR", "name": "South Korea"},
    {"acronym": "KW", "name": "Kuwait"},
    {"acronym": "KY", "name": "Cayman Islands"},
    {"acronym": "KZ", "name": "Kazakhstan"},
    {"acronym": "LA", "name": "Lao People's Democratic Republic"},
    {"acronym": "LB", "name": "Lebanon"},
    {"acronym": "LC", "name": "Saint Lucia"},
    {"acronym": "LI", "name": "Liechtenstein"},
    {"acronym": "LK", "name": "Sri Lanka"},
    {"acronym": "LR", "name": "Liberia"},
    {"acronym": "LS", "name": "Lesotho"},
    {"acronym": "LT", "name": "Lithuania"},
    {"acronym": "LU", "name": "Luxembourg"},
    {"acronym": "LV", "name": "Latvia"},
    {"acronym": "LY", "name": "Libya"},
    {"acronym": "MA", "name": "Morocco"},
    {"acronym": "MC", "name": "Monaco"},
    {"acronym": "MD", "name": "Moldova"},
    {"acronym": "ME", "name": "Montenegro"},
    {"acronym": "MF", "name": "Saint Martin"},
    {"acronym": "MG", "name": "Madagascar"},
    {"acronym": "MH", "name": "Marshall Islands"},
    {"acronym": "MK", "name": "North Macedonia"},
    {"acronym": "ML", "name": "Mali"},
    {"acronym": "MM", "name": "Myanmar"},
    {"acronym": "MN", "name": "Mongolia"},
    {"acronym": "MO", "name": "Macau"},
    {"acronym": "MP", "name": "Northern Mariana Islands"},
    {"acronym": "MQ", "name": "Martinique"},
    {"acronym": "MR", "name": "Mauritania"},
    {"acronym": "MS", "name": "Montserrat"},
    {"acronym": "MT", "name": "Malta"},
    {"acronym": "MU", "name": "Mauritius"},
    {"acronym": "MV", "name": "Maldives"},
    {"acronym": "MW", "name": "Malawi"},
    {"acronym": "MX", "name": "Mexico"},
    {"acronym": "MY", "name": "Malaysia"},
    {"acronym": "MZ", "name": "Mozambique"},
    {"acronym": "NA", "name": "Namibia"},
    {"acronym": "NC", "name": "New Caledonia"},
    {"acronym": "NE", "name": "Niger"},
    {"acronym": "NF", "name": "Norfolk Island"},
    {"acronym": "NG", "name": "Nigeria"},
    {"acronym": "NI", "name": "Nicaragua"},
    {"acronym": "NL", "name": "Netherlands"},
    {"acronym": "NO", "name": "Norway"},
    {"acronym": "NP", "name": "Nepal"},
    {"acronym": "NR", "name": "Nauru"},
    {"acronym": "NU", "name": "Niue"},
    {"acronym": "NZ", "name": "New Zealand"},
    {"acronym": "O1", "name": "Other"},
    {"acronym": "OM", "name": "Oman"},
    {"acronym": "PA", "name": "Panama"},
    {"acronym": "PE", "name": "Peru"},
    {"acronym": "PF", "name": "French Polynesia"},
    {"acronym": "PG", "name": "Papua New Guinea"},
    {"acronym": "PH", "name": "Philippines"},
    {"acronym": "PK", "name": "Pakistan"},
    {"acronym": "PL", "name": "Poland"},
    {"acronym": "PM", "name": "Saint Pierre and Miquelon"},
    {"acronym": "PN", "name": "Pitcairn"},
    {"acronym": "PR", "name": "Puerto Rico"},
    {"acronym": "PS", "name": "State of Palestine"},
    {"acronym": "PT", "name": "Portugal"},
    {"acronym": "PW", "name": "Palau"},
    {"acronym": "PY", "name": "Paraguay"},
    {"acronym": "QA", "name": "Qatar"},
    {"acronym": "RE", "name": "Reunion"},
    {"acronym": "RO", "name": "Romania"},
    {"acronym": "RS", "name": "Serbia"},
    {"acronym": "RU", "name": "Russian Federation"},
    {"acronym": "RW", "name": "Rwanda"},
    {"acronym": "SA", "name": "Saudi Arabia"},
    {"acronym": "SB", "name": "Solomon Islands"},
    {"acronym": "SC", "name": "Seychelles"},
    {"acronym": "SD", "name": "Sudan"},
    {"acronym": "SE", "name": "Sweden"},
    {"acronym": "SG", "name": "Singapore"},
    {"acronym": "SH", "name": "Saint Helena"},
    {"acronym": "SI", "name": "Slovenia"},
    {"acronym": "SJ", "name": "Svalbard and Jan Mayen"},
    {"acronym": "SK", "name": "Slovakia"},
    {"acronym": "SL", "name": "Sierra Leone"},
    {"acronym": "SM", "name": "San Marino"},
    {"acronym": "SN", "name": "Senegal"},
    {"acronym": "SO", "name": "Somalia"},
    {"acronym": "SR", "name": "Suriname"},
    {"acronym": "ST", "name": "Sao Tome and Principe"},
    {"acronym": "SV", "name": "El Salvador"},
    {"acronym": "SX", "name": "Sint Maarten"},
    {"acronym": "SY", "name": "Syrian Arab Republic"},
    {"acronym": "SZ", "name": "Eswatini"},
    {"acronym": "TC", "name": "Turks and Caicos Islands"},
    {"acronym": "TD", "name": "Chad"},
    {"acronym": "TF", "name": "French Southern Territories"},
    {"acronym": "TG", "name": "Togo"},
    {"acronym": "TH", "name": "Thailand"},
    {"acronym": "TJ", "name": "Tajikistan"},
    {"acronym": "TK", "name": "Tokelau"},
    {"acronym": "TL", "name": "Timor-Leste"},
    {"acronym": "TM", "name": "Turkmenistan"},
    {"acronym": "TN", "name": "Tunisia"},
    {"acronym": "TO", "name": "Tonga"},
    {"acronym": "TR", "name": "Türkiye"},
    {"acronym": "TT", "name": "Trinidad and Tobago"},
    {"acronym": "TV", "name": "Tuvalu"},
    {"acronym": "TW", "name": "Taiwan"},
    {"acronym": "TZ", "name": "United Republic of Tanzania"},
    {"acronym": "UA", "name": "Ukraine"},
    {"acronym": "UG", "name": "Uganda"},
    {"acronym": "UM", "name": "United States Minor Outlying Islands"},
    {"acronym": "US", "name": "United States"},
    {"acronym": "UY", "name": "Uruguay"},
    {"acronym": "UZ", "name": "Uzbekistan"},
    {"acronym": "VA", "name": "Holy See (Vatican City State)"},
    {"acronym": "VC", "name": "Saint Vincent and the Grenadines"},
    {"acronym": "VE", "name": "Venezuela"},
    {"acronym": "VG", "name": "Virgin Islands, British"},
    {"acronym": "VI", "name": "Virgin Islands, U.S."},
    {"acronym": "VN", "name": "Vietnam"},
    {"acronym": "VU", "name": "Vanuatu"},
    {"acronym": "WF", "name": "Wallis and Futuna"},
    {"acronym": "WS", "name": "Samoa"},
    {"acronym": "XK", "name": "Kosovo"},
    {"acronym": "XX", "name": "Unknown"},
    {"acronym": "YE", "name": "Yemen"},
    {"acronym": "YT", "name": "Mayotte"},
    {"acronym": "ZA", "name": "South Africa"},
    {"acronym": "ZM", "name": "Zambia"},
    {"acronym": "ZW", "name": "Zimbabwe"}
]


country_stats = defaultdict(lambda: {
    "ipv4_count": 0,
    "ipv6_count": 0,
    "ipv4_blocks": 0,
    "ipv6_blocks": 0
})

with maxminddb.open_database("./GeoLite2-Country.mmdb") as country_reader:
    for network, record in country_reader:
        try:
            net = ipaddress.ip_network(network)
        except ValueError:
            continue  # 忽略不合法的 IP 段

        num_ips = net.num_addresses
        is_ipv6 = net.version == 6

        country_info = record.get("country")
        if not country_info:
            country = "XX"  # 未知国家
        else:
            country = country_info.get("iso_code", "XX")

        # 分别统计 IPv4 和 IPv6
        if is_ipv6:
            country_stats[country]["ipv6_count"] += num_ips
            country_stats[country]["ipv6_blocks"] += 1
        else:
            country_stats[country]["ipv4_count"] += num_ips
            country_stats[country]["ipv4_blocks"] += 1


for country, stats in sorted(country_stats.items(), key=lambda x: x[1]["ipv4_blocks"], reverse=True):
    print(f"{country}:")
    print(
        f"  IPv4: {stats['ipv4_count']:,} IPs in {stats['ipv4_blocks']:,} blocks")
    print(
        f"  IPv6: {stats['ipv6_count']:,} IPs in {stats['ipv6_blocks']:,} blocks")

lines = []
lines.append(
    "| ISO | Flag | Country | IPv4 Block | IPv4 Count | IPv6 Block | IPv6 Count |")
lines.append("| :---: | :---: | --- | :---: | :---: | :---: | :---: |")


for country_code, stats in sorted(country_stats.items(), key=lambda x: x[1]["ipv4_blocks"], reverse=True):
    name = next((c['name'] for c in country_list if c['acronym']
                == country_code), country_code)
    flag = f'<img src="/flags/{country_code}.png" width="35" valign="middle"/>'

    ipv6_count = f'{stats["ipv6_count"]:.2e}'  # 科学计数法
    line = f'| {country_code} | {flag} | {name} | {stats["ipv4_blocks"]:,} | {stats["ipv4_count"]:,} | {stats["ipv6_blocks"]:,} | {ipv6_count} |'
    lines.append(line)

markdown = "\n".join(lines)


readme_path = "README.md"
if not os.path.exists(readme_path):
    content = "# 🌐 IP Address Statistics by Country\n\n" + markdown + "\n"
else:
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    marker = "| ISO | Flag | Country | IPv4 Block | IPv4 Count | IPv6 Block | IPv6 Count |"
    if marker in content:
        start = content.index(marker)
        end = content.find("\n\n", start)
        if end == -1:
            end = len(content)
        content = content[:start] + markdown + content[end:]
    else:
        content += "\n\n" + markdown

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ README.md updated!")
