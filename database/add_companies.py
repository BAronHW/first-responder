# ================================================================
# This script adds company data to the companies table in jobs.db.
# ================================================================

import sqlite3

con = sqlite3.connect("database/JOBS.db")
cursor = con.cursor()

COMPANY = ""
LINK = ""
TYPE = ""

# cursor.execute(
#     "INSERT INTO companies (company, link, type) VALUES (?, ?, ?)",
#     (COMPANY, LINK, TYPE),
# )

cursor.executescript(
    """UPDATE companies
    SET link = 'https://ghr.wd1.myworkdayjobs.com/en-US/Lateral-US?locations=13a0897a1ccc103909354037339cac3f&locations=13a0897a1ccc10390935432110b3ac7b&locations=13a0897a1ccc1039093544185095ac8f&locations=13a0897a1ccc10390935492af03bacf8&locations=13a0897a1ccc103909354a5ec592ad11&locations=13a0897a1ccc103909354b545cdfad25&locations=13a0897a1ccc103909354bcfd278ad2f&locations=13a0897a1ccc103909354c88c68cad3e&locations=13a0897a1ccc103909354d032589ad48&locations=13a0897a1ccc103909354df0d2aead57&locations=13a0897a1ccc103909354e6be0b4ad61&locations=13a0897a1ccc1039093551cfb672ada7&locations=13a0897a1ccc10390935528a9029adb6&locations=13a0897a1ccc1039093553441af0adc5&locations=13a0897a1ccc1039095350308fa0af50&locations=13a0897a1ccc10390953588daa43affa&locations=13a0897a1ccc10390971dd511b10b031&locations=13a0897a1ccc10390971e17e16a5b081&locations=09ce913814b6012043b9cc737a5a2c6a&locations=9637d9bad6051018b6352ab0462d0000&locations=42cd3166f63110177f6292561e5b0000&locations=13a0897a1ccc103909179149ee3fab07&locations=13a0897a1ccc10390935416c6a95ac58&locations=13a0897a1ccc1039093547f46a11acdf&locations=13a0897a1ccc1039093549a652e1ad02&locations=13a0897a1ccc103909354b16cbcfad20&locations=13a0897a1ccc10390971dfc40eb4b05e&locations=13a0897a1ccc1039093551167fddad98&locations=07b8ebe5823b102010423968b7b10000&locations=e05d17d1021e100fbfc9b2a62abb0000&locations=2fcbf0f85bda015f5d3a65f4e36708ba&locations=13a0897a1ccc10390991bf0a677cb3f4&locations=2fcbf0f85bda01b52462d4a1e367e4b2&locations=13a0897a1ccc103909178fc08786aae8&locations=13a0897a1ccc10390728ed66e0837f8f&locations=13a0897a1ccc1039073a9fc9d72081c0&locations=13a0897a1ccc1039073aa673f4e9823d&locations=13a0897a1ccc1039073aa80c677b825b&locations=13a0897a1ccc10390728ebb3635c7f6c&locations=13a0897a1ccc1039074cde5df91882ec&locations=2fcbf0f85bda019f5bc450d1e167757d&timeType=763d0bf7c064103624b3019f084b007d'
    WHERE company = 'Bank of America';"""
)

con.close()
