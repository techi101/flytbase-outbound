"""Builds site/index.html and accounts.csv from the account list below.

Every trigger was read from the linked public source on 26 Nov 2026.
Buyer column holds job roles only. No personal names, emails or phone numbers.
"""
import csv
import html
from pathlib import Path

ROOT = Path(__file__).parent

# ---- Sources (publisher, date, url) -------------------------------------
S = {
    "meed_rtc": ("MEED, 14 Jul 2026", "https://www.meed.com/masdar-reaches-financial-close-on-world-first-247-solar-project"),
    "zarraf": ("Construction Review, Jun 2025", "https://constructionreviewonline.com/edf-and-kowepo-ink-deal-for-1-5-gw-al-zarraf-solar-pv-project-in-abu-dhabi/"),
    "manah1": ("Power Technology", "https://www.power-technology.com/projects/manah-i-solar-power-plant-oman/"),
    "edf_manah1": ("EDF power solutions", "https://france.edf-powersolutions.com/communiques/edf-renewables-and-korea-western-power-company-inaugurate-sultanate-of-omans-largest-solar-power-plant/"),
    "round7": ("GCC Tender News citing MEED, 22 Nov 2026", "https://gcctendernews.com/article/saudi-nrep-round-7-solar-ipps-four-frontrunners-meed-reports/"),
    "khazna": ("Construction Review, 30 Jan 2026", "https://constructionreviewonline.com/construction-begins-on-1-5-gw-khazna-solar-pv-project/"),
    "nama_ar": ("Nama PWP Annual Report 2025", "https://omanpwp.om/storage/files/1/annual-report/6a3b71d52252a.pdf"),
    "ad_storage": ("ESS News, 24 Sep 2026", "https://www.ess-news.com/2026/09/24/abu-dhabi-targets-15-gw-of-energy-storage-by-2035/"),
    "acwa_fc": ("Energetica India, 2 Oct 2024", "https://www.energetica-india.net/news/acwa-power-and-partners-secure-financial-close-on-solar-projects"),
    "redsea": ("PV Tech, 8 Sep 2026", "https://www.pv-tech.org/acwa-power-starts-commercial-operations-340mw-off-grid-solar-plus-storage-project/"),
    "redsea_an": ("Arab News, 6 Sep 2026", "https://www.arabnews.com/energy/saudi-red-sea-destination-begins-operations-with-giant-off-grid-renewable-energy-system-3000732"),
    "dewa": ("DEWA, 14 Jan 2026", "https://dewa.gov.ae/en/about-us/media-publications/latest-news/2026/1/dewa-highlights-7th-phase"),
    "dukhan": ("Energy Global, 22 Sep 2025", "https://www.energyglobal.com/solar/22092025/qatarenergy-signs-solar-plant-construction-contract-with-samsung/"),
    "kharsaah": ("TotalEnergies", "https://totalenergies.com/company/projects/solar/al-kharsaah-solar-power-plant-qatar"),
    "ibri3": ("Masdar", "https://masdar.ae/en/news/newsroom/nama-power-and-water-procurement-signs-agreement-with-masdar-led-consortium"),
    "ibri3_meed": ("MEED, 22 Sep 2025", "https://www.meed.com/oman-awards-403m-ibri-iii-solar-ipp-contract"),
    "kuwait": ("MVA Pulse, 18 Aug 2026", "https://www.mvapulse.com/mena-renewable-energy-kuwait-awards-1-1-gw-solar-project/"),
    "bahrain": ("PV Tech, 20 Oct 2025", "https://www.pv-tech.org/bahrain-launches-tender-100mw-solar-project/"),
}

# ---- Accounts -----------------------------------------------------------
# tier: A = site running or being built now, B = awarded or financed, C = watch (bid stage)
ACCOUNTS = [
    dict(name="Masdar", country="UAE", tier="A",
         trigger="Reached financial close on 13 Jul 2026 for the round-the-clock project with EWEC: 5.2 GW of PV plus 19 GWh of batteries, US$6.1bn.",
         src=["meed_rtc"],
         buyer="Head of asset management or O&M for UAE renewables",
         line="Saw the round-the-clock project close its financing in July. With 5.2 GW of panels next to 19 GWh of batteries, I am guessing the inspection plan for that site is still being written."),
    dict(name="EDF power solutions, Middle East", country="UAE", tier="A",
         trigger="Runs Manah 1 (500 MW, Oman, with KOWEPO, commissioned Jan 2025). Signed 1.5 GW Al Zarraf in Abu Dhabi (Jun 2025). Reported Round 7 frontrunner in Saudi (Nov 2026).",
         src=["edf_manah1", "zarraf", "round7"],
         buyer="Regional O&M director, or asset manager for Manah 1",
         line="You now run Manah 1 in Oman and have Al Zarraf coming in Al Dhafra, two big desert sites far apart. Is the plan to inspect both from one control room?"),
    dict(name="Jinko Power", country="UAE", tier="A",
         trigger="In the consortium building 1.5 GW Khazna Solar PV (civil works began Jan 2026, operation planned 2027). Partner in Manah II, Oman (500 MW, running since Q2 2025).",
         src=["khazna", "nama_ar"],
         buyer="Head of O&M, Middle East",
         line="Civil works started at Khazna in January, and Manah II has been running since last year. How does your team do thermography on a 500 MW site today, drones with a pilot or crews on foot?"),
    dict(name="TAQA", country="UAE", tier="A",
         trigger="In the consortium building 1.5 GW Khazna Solar PV in Abu Dhabi, construction began Jan 2026.",
         src=["khazna"],
         buyer="Head of security and HSE for generation assets",
         line="Khazna moving into construction caught my eye. Once it is live, who on the TAQA side will own perimeter security for a 1.5 GW site out in the desert?"),
    dict(name="EWEC", country="UAE", tier="B",
         trigger="Offtaker and co-developer on Khazna, Al Zarraf and the round-the-clock project. Abu Dhabi set a 15 GW storage target for 2035 (Sep 2026).",
         src=["ad_storage", "meed_rtc"],
         buyer="Renewables asset oversight or digital operations lead",
         line="EWEC buys the power from every big solar plant in Abu Dhabi. Do you set any shared standard for how those plants get inspected, or is that left to each developer?"),
    dict(name="ACWA Power", country="Saudi Arabia", tier="B",
         trigger="Financed Haden (2 GW), Muwayh (2 GW) and Al Khushaybi (1.5 GW) with Badeel and Aramco Power; commercial operation expected Q1 2027.",
         src=["acwa_fc"],
         buyer="VP operations and maintenance, renewables",
         line="Haden, Muwayh and Al Khushaybi are due in early 2027, which is 5.5 GW arriving almost at once. Has the O&M team already decided how thermal checks will run across three sites?"),
    dict(name="Red Sea Global", country="Saudi Arabia", tier="A",
         trigger="Off-grid utility system went into full commercial operation in Sep 2026: about 340 MW of PV and 1,227 MWh of batteries feeding the airport and resorts.",
         src=["redsea", "redsea_an"],
         buyer="Director of utilities, or head of destination security",
         line="Congrats on the Red Sea utilities going fully off grid in September. With the airport and resorts on the same system, are solar inspection and site security still two separate teams?"),
    dict(name="Aljomaih Energy and Water (with TotalEnergies)", country="Saudi Arabia", tier="C",
         trigger="Reported by MEED as a frontrunner for one of four Round 7 solar IPPs (Tabjal 2, Mawqqaq, Tathleeth, South Al-Ula). Not yet confirmed.",
         src=["round7"],
         buyer="Head of O&M or technical director",
         line="MEED has Aljomaih and TotalEnergies among the Round 7 frontrunners. If one of those plants lands with you, now is the cheap moment to plan how it gets inspected."),
    dict(name="Etihad Water and Electricity (with KEPCO)", country="UAE", tier="C",
         trigger="Reported Round 7 solar frontrunner in Saudi Arabia with KEPCO (Nov 2026). Not yet confirmed.",
         src=["round7"],
         buyer="Head of business development, renewables",
         line="Read that EtihadWE and KEPCO are among the Round 7 frontrunners. If that plant comes your way, I would love to hear how you plan to run it from across the border."),
    dict(name="DEWA", country="UAE", tier="B",
         trigger="Mohammed bin Rashid Solar Park is at 3,860 MW; Phase 7 tender adds 2 GW PV plus 1,400 MW of six-hour storage (Jan 2026).",
         src=["dewa"],
         buyer="Solar park operations or innovation lead",
         line="The solar park is at 3,860 MW and Phase 7 adds another 2 GW with batteries. That is a lot of rows to walk in a Dubai summer."),
    dict(name="QatarEnergy Renewable Solutions", country="Qatar", tier="B",
         trigger="Signed with Samsung C&T to build the 2 GW Dukhan solar plant by mid-2029, which doubles Qatar's solar capacity (Sep 2025).",
         src=["dukhan"],
         buyer="Asset manager, solar",
         line="Dukhan doubles Qatar's solar capacity by 2029, and Al Kharsaah is already running in the same part of the country. Are you planning one inspection setup for both?"),
    dict(name="Samsung C&T (Dukhan EPC)", country="Qatar", tier="A",
         trigger="EPC contractor building the 2 GW Dukhan plant through mid-2029.",
         src=["dukhan"],
         buyer="Project director or construction QA lead",
         line="Building 2 GW at Dukhan means a lot of weekly progress reports. A drone centre in Oman cut its reporting time by 87% on government sites with no pilot on site, and I can share how."),
    dict(name="Siraj Energy / Al Kharsaah (TotalEnergies, Marubeni)", country="Qatar", tier="A",
         trigger="800 MWp running since Oct 2022, two million bifacial modules on trackers, modules cleaned every four days. No new trigger; the size of the O&M job is the reason.",
         src=["kharsaah"],
         buyer="Plant manager",
         line="Al Kharsaah has two million bifacial modules and cleans every one of them every four days. Do the thermal checks run on a schedule that tight too?"),
    dict(name="Sembcorp (Manah II)", country="Oman", tier="A",
         trigger="Manah II (500 MW, Sembcorp Jinko Shine) reached commercial operation in Q2 2025.",
         src=["nama_ar"],
         buyer="Asset manager, Oman",
         line="Manah II hit commercial operation in Q2 2025. About a year in, how is your team handling string level inspections across 500 MW?"),
    dict(name="OQ Alternative Energy", country="Oman", tier="B",
         trigger="In the Masdar-led consortium for Ibri III: 500 MW PV plus 100 MWh battery, Oman's first utility solar with storage. Contract signed Sep 2025.",
         src=["ibri3", "ibri3_meed"],
         buyer="Head of operations or digital lead",
         line="Ibri III is Oman's first solar plant with a battery yard. Has the team looked at one docked drone covering both the PV rows and the BESS?"),
    dict(name="Masdar, Kuwait project team", country="Kuwait", tier="B",
         trigger="Masdar-led consortium won the 1.1 GW Al Dibdibah and Shagaya Phase III Zone 1 solar project (Aug 2026).",
         src=["kuwait"],
         buyer="Project director, Kuwait",
         line="Congrats on Al Dibdibah. With sites now in the UAE, Oman and Kuwait, is Masdar thinking about one remote inspection setup across all of them?"),
    dict(name="Bahrain EWA (Bilaj Al Jazayer bidders)", country="Bahrain", tier="C",
         trigger="EWA tendered a 100 MW solar IPP at Bilaj Al Jazayer, due online by Sep 2027 (Oct 2025). Watch for the award.",
         src=["bahrain"],
         buyer="The winning developer's plant manager",
         line="Bilaj Al Jazayer is due by September 2027. A 100 MW plant usually runs with a small team, which is where remote inspection helps most."),
]

SEQUENCE = [
    ("Day 1", "Email", "Trigger first",
     "Subject: {site} inspections\n\nHi {first},\n\n{first line from the table}\n\nEnBW grew its solar fleet from 150 MW to 1 GW and now runs drone inspections from Stuttgart, with docks on site and no one driving out. They got 2 to 4 times more inspections for the same budget.\n\nWorth a 15 minute look for {site}?"),
    ("Day 3", "LinkedIn", "Connect, no pitch",
     "Hi {first}, I work with teams running docked drones on large solar sites. Saw the {trigger} news and wanted to follow your work on it."),
    ("Day 8", "Email", "A different proof",
     "Subject: no pilot on site\n\nHi {first},\n\nOne more example closer to home. Ibn Firnas Drone Center in Oman watches three government sites from one hub over Starlink, with no pilot on any site. Reporting time dropped 87%.\n\nRemote desert sites are the same problem. If useful I can send a one page sketch of where docks would sit on {site}."),
    ("Day 15", "Email", "Close the loop",
     "Subject: closing this out\n\nHi {first},\n\nI will stop here. If inspections at {site} come up for review next year, reply with 'later' and I will check back then. If someone else owns this, a name would help a lot."),
]


def esc(s):
    return html.escape(s, quote=True)


def tok(s):
    import re
    return re.sub(r"\{([^}]+)\}", lambda m: '<span class="tok">' + m.group(1) + '</span>', s)


def src_links(keys):
    return " ".join(
        f'<a href="{esc(S[k][1])}" target="_blank" rel="noopener">{esc(S[k][0])}</a>' for k in keys
    )


def rows_html():
    out = []
    for i, a in enumerate(ACCOUNTS):
        out.append(f"""
      <tr data-country="{esc(a['country'])}">
        <td class="acc" data-label="Account"><span class="tier t{a['tier']}" title="Tier {a['tier']}">{a['tier']}</span><strong>{esc(a['name'])}</strong><span class="ctry">{esc(a['country'])}</span></td>
        <td class="trg" data-label="Trigger">{esc(a['trigger'])}<span class="src">{src_links(a['src'])}</span></td>
        <td class="buy" data-label="Who to reach">{esc(a['buyer'])}</td>
        <td class="fl" data-label="First line"><p id="l{i}">{esc(a['line'])}</p><button class="copy" type="button" data-for="l{i}">Copy line</button></td>
      </tr>""")
    return "".join(out)


def seq_html():
    out = []
    for day, ch, title, body in SEQUENCE:
        out.append(f"""
      <li>
        <div class="when"><span class="day">{day}</span><span class="ch">{ch}</span></div>
        <div class="what"><h3>{esc(title)}</h3><pre>{tok(esc(body))}</pre></div>
      </li>""")
    return "".join(out)


def countries():
    seen = []
    for a in ACCOUNTS:
        if a["country"] not in seen:
            seen.append(a["country"])
    return seen


def chips():
    c = ['<button type="button" class="chip" aria-pressed="true" data-c="all">All {}</button>'.format(len(ACCOUNTS))]
    for k in countries():
        n = sum(1 for a in ACCOUNTS if a["country"] == k)
        c.append(f'<button type="button" class="chip" aria-pressed="false" data-c="{esc(k)}">{esc(k)} {n}</button>')
    return "".join(c)


def main():
    tpl = (ROOT / "template.html").read_text(encoding="utf-8")
    page = (tpl.replace("{{ROWS}}", rows_html())
               .replace("{{SEQ}}", seq_html())
               .replace("{{CHIPS}}", chips())
               .replace("{{N}}", str(len(ACCOUNTS))))
    (ROOT / "site" / "index.html").write_text(page, encoding="utf-8")
    with open(ROOT / "accounts.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["account", "country", "tier", "trigger", "buyer_role", "first_line", "sources"])
        for a in ACCOUNTS:
            w.writerow([a["name"], a["country"], a["tier"], a["trigger"], a["buyer"], a["line"],
                        " | ".join(S[k][1] for k in a["src"])])
    (ROOT / "site" / "accounts.csv").write_bytes((ROOT / "accounts.csv").read_bytes())
    print("built", len(ACCOUNTS), "accounts")


if __name__ == "__main__":
    main()
