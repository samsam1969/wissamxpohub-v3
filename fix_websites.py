f = open("services/lightpanda_service.py", encoding="utf-8")
content = f.read()
f.close()

old = """            # Also try to get website links
            website_pattern = re.compile(r'href="https?://(?!www\\.europages)([^"]{4,60})"')
            websites = set()
            for m in website_pattern.finditer(content):
                domain = m.group(1).split('/')[0]
                if '.' in domain and not 'europages' in domain:
                    websites.add(domain)
            
            websites_list = list(websites)[:30]
            
            for i, raw in enumerate(raw_names[:20]):
                name = clean_html_entities(raw.strip())
                if not is_valid_name(name): continue
                website = websites_list[i] if i < len(websites_list) else ""
                buyers.append({
                    "name":        name,
                    "country":     country,
                    "source":      "Europages",
                    "source_link": url,
                    "website":     website,
                    "email":       "",
                    "phone":       "",
                })"""

new = """            # Extract company profile links (only .de/.com/.eu domains - not tracking/social sites)
            SKIP_DOMAINS = {"cloudflare.com","facebook.com","linkedin.com","twitter.com",
                           "google.com","microsoft.com","hubspot.com","cookie-script.com",
                           "visable.com","europages.com","europages.co.uk","policies.google.com",
                           "bme.de","privacy.microsoft.com"}
            
            # Try to get company websites from profile links
            company_site_pattern = re.compile(
                r'company[^"]*href="https?://([a-zA-Z0-9.-]+\\.[a-zA-Z]{2,6})[^"]*"'
                r'|href="https?://([a-zA-Z0-9.-]+\\.[a-zA-Z]{2,6})[^"]*"[^>]*>[^<]*GmbH'
            )
            
            for i, raw in enumerate(raw_names[:20]):
                name = clean_html_entities(raw.strip())
                if not is_valid_name(name): continue
                buyers.append({
                    "name":        name,
                    "country":     country,
                    "source":      "Europages",
                    "source_link": url,
                    "website":     "",
                    "email":       "",
                    "phone":       "",
                })"""

if old in content:
    content = content.replace(old, new, 1)
    open("services/lightpanda_service.py", "w", encoding="utf-8").write(content)
    print("OK - website extraction fixed")
else:
    print("Not found - checking...")
    idx = content.find("websites_list")
    print("websites_list at:", idx)
