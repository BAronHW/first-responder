# First Responder
Doesn't the job market suck? A lot? It's so hard trying to get a job right now, let alone **find** one that matches your skills and experience. That's why I built First Responder.

First Responder scrapes jobs from any company careers site that you want and sends a tailored list of them to a Discord server of your choosing. For now, the tailoring is done by filtering jobs based on a set of filtered words.

If you want to see my plans for the future, check out the bottom of this README for a better look!

If you are a non-technical user and think you will be confused about everything below, check out the [instructions for non-technical users](markdown/NON_TECHNICAL_INSTRUCTIONS.md), as I explain a **lot** of information in it from installing git to running the project locally.

# Setup
I highly suggest forking this repo rather than cloning it first because the driving factor is using the GitHub Actions workflow I've set up with the cron job to scrape every 2 hours.

## Renaming files
Change the file name of `.env.example` to `.env`
```{bash}
git mv .env.example .env
```
and the name of `COMPANIES_TEMPLATE.md` to `COMPANIES.md`
```{bash}
git mv markdown/COMPANIES_TEMPLATE.md markdown/COMPANIES.md
```

## Discord webhook
On a Discord server you'd like to use, create a new channel called `first-responder` and create a new webhook named "First Responder".

Then go into your `.env` file and and add it to `DISCORD_WEBHOOK`, and then as a GitHub Actions secret.

## Neon PostgreSQL database
Create a new project and add the connection string to your `.env` file for the `DATABASE_URL` variable, and then as a GitHub Actions secret.

After setting up the project, go into the "SQL Editor" and execute the following SQL statements to create the `companies` and `seen` tables.

```{SQL}
CREATE TABLE companies (
    company TEXT NOT NULL,
    link TEXT NOT NULL,
    type TEXT NOT NULL,
    UNIQUE(company, link, type)
);
```
```{SQL}
CREATE TABLE seen (
    company TEXT NOT NULL,
    title TEXT NOT NULL,
    link TEXT NOT NULL,
    date TEXT NOT NULL,
    UNIQUE(company, title, link, date)
);
```
## Adding companies
What is this `COMPANIES.md` file? Use it or don't use it, it's up to you, but it is where you can keep a quick and easy list of companies and their career's page URL so you can keep track of it. More importantly, I'm assuming if you're reading this then you do not have a list of companies with their exact careers links ready to go. If you spend some time making a big list of companies and their links, you can add it to that file and use it to put all the information into the database at once using 1 `INSERT` statement.

To find these companies, you can enter the following `site:` into a search engine to find all links that match the careers page. This is best for the job boards, but not custom scrapers (the companies that do not use a dedicated job board like workday, ashby, or greenhouse).
- **Workday:** site:wd1.myworkdayjobs.com
- **Ashby:** site:jobs.ashbyhq.com
- **Greenhouse:** site:job-boards.greenhouse.io

If you fill out that file with companies, you can ask AI the following prompt to get a PostgreSQL statement to insert the massive list of companies into the `companies` table all at once on Neon.
```{prompt}
Using the attached COMPANIES.md, give me a single PostgreSQL INSERT statement that inserts all companies into a table called companies with columns company, link, and type (which is the job board: workday, ashby, greenhouse, hackernews, or custom).
```

## Setting your own filters
To set the allow and deny filters for job title searches, go to the file `filter/filters.py` and change the preset filters.

These are not case sensitive, as all job titles become lowercase, but make sure to get all "versions" of what might be in a job title (i.e. junior, jr., jr).

The `allow` list is what will be included from matches, and the `deny` list is what will be excluded from matches.

# Running the scraper locally
```{bash}
uv sync
```
```{bash}
uv run playwright install
```
```{bash}
uv run main.py
```

# What's next for First Responder?
- Incorporate a small LLM (most likely qwen3.5:9b) using an online GPU provider to get job results more tailored to the user. This will pick jobs based on title, then look at the job description and only send the job if the description fits the users profile.
- Add the ability to send text reminders using Twilio so that the user can remember to check Discord if they need better reminding or don't have Discord notifications turned on.
- Add the ability to make First Responder local first. That means local LLM (most likely using a smaller model <4b), local database, and no Twilio support.