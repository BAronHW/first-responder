# First Responder
Doesn't the job market suck? A lot? It's so hard trying to get a job right now, let alone *find* one that matches your skills and experience. That's why I built First Responder.

First Responder scrapes jobs from any company careers site that you want and sends a tailored list of them to a Discord server of your choosing. For now, the tailoring is done by filtering jobs based on set filterd words.

There are lots of plans in the works to make this even better, so right now First Responder is in it's MVP stage. The current goal is to just send filtered out jobs to yourself, but in the future the goal will be that 100% of the jobs sent are jobs you would **for sure** want to apply to. That would mean the title sounds like something you're looking for and, more importantly, the description fits too.

If you want to see my plans for the future, check out the bottom of this README for a better look!

# Setup
Before setting up the environment variables, let's first change some of the file names.

After cloning this repo and making sure you're in the directory for `first-responder`, change the file name of `.env.example` to `.env`
```{bash}
git mv .env.example .env
```
and then change the file name of `COMPANIES_TEMPLATE.md` to `COMPANIES.md`
```{bash}
git mv markdown/COMPANIES_TEMPLATE.md markdown/COMPANIES.md
```

What is this `COMPANIES.md` file? Use it or don't use it, it's up to you, but it is where you can keep a quick and easy list of companies and their career's page URL so you can keep track of it. More importantly, I'm assuming if you're reading this then you do not have a list of companies with their exact careers links ready to go. If you spend some time finding a big list of companies and their links, you can add it to that file and use it to put all the information into the database at once (more information on that later).

To find these companies, you can enter the following `site:` into a search engine to find all links that match the careers page. This is best for the job boards, but not custom scrapers (the companies that do not use a dedicated job board like greenhouse or ashby).
- **Workday:** site:wd1.myworkdayjobs.com
- **Ashby:** site:jobs.ashbyhq.com
- **Greenhouse:** site:job-boards.greenhouse.io

## Discord Webhook
On a Discord server you'd like to use (I'd suggest creating one for this project if you don't have one available), create a new channel called `first-responder` and create a new webhook named "First Responder". If you don't know how to do this, follow this order after creating a channel:
- Edit Channel (gear icon) -> Integrations -> Webhooks -> New Webhook -> Click on new webhook

Once you have the webhook URL copied, go into your `.env` file and and add it to `DISCORD_WEBHOOK`. Then, after creating a GitHub repo for your clone (maybe best option is to fork this repo for ease of use), add this as a GitHub Actions Secret. If you don't know how to do this, follow this order once you've set up your repository:
- Settings -> Secrets and variables -> Actions -> New repository secret -> then "Name" should be "DISCORD_WEBHOOK" and the "Secret" should be your copied Discord webhook URL.

## Neon PostgreSQL Database
If you don't already have a [Neon](https://neon.com) account, go ahead and create one. For this project, the free trial will be enough, and we will use this for serverless PostgreSQL.

Once you have an account, create a new project and add the connection string to your `.env` file for the `DATABASE_URL` variable. If you don't know how to set up a project on Neon and get this connection string, follow this order after having an account:
- New Project -> type "First Responder" for Project name -> Create -> Connection string -> then press the "copy snippet" button below the connection string.

Set up the GitHub Actions Secret the same way you did for Discord, where the "Name" is "DATABASE_URL" and the "Secret" is that connection string.

After setting up the project, go into the "SQL Editor" tab on the left and run the following SQL statements separately.

To create the table `companies` run
```{SQL}
CREATE TABLE companies (
    company TEXT NOT NULL,
    link TEXT NOT NULL,
    type TEXT NOT NULL,
    UNIQUE(company, link, type)
);
```

To create the table `seen` run
```{SQL}
CREATE TABLE seen (
    company TEXT NOT NULL,
    title TEXT NOT NULL,
    link TEXT NOT NULL,
    date TEXT NOT NULL,
    UNIQUE(company, title, link, date)
);
```

Do you remember that `COMPANIES.md` file from earlier? If you fill out that file with companies, you can ask AI the follow prompt to get a PostgreSQL statement to insert the massive list of companies into the `companies` table all at once on Neon.
```{prompt}
Using the attached COMPANIES.md, give me a single PostgreSQL INSERT statement that inserts all companies into a table called companies with columns company, link, and type (which is the job board: workday, ashby, greenhouse, hackernews, or custom).
```

Neon is great because after we have our 2 tables filled, we can view the tables directly online without needing to install any database software like pgAdmin. You can also very easily add one-off companies to the list if you find one later on.

# Running the scraper
- Once everything is set up (Discord webhook on a channel, Neon connection string with a project, Postgres tables set up, GH actions secrets set up, all modified code in your repo) you can now run the scraper locally to test it out!

Ensure `uv` is installed, then in the project directory run
```{bash}
uv sync
```
then
```{bash}
uv run playwright install
```
and finally
```{bash}
uv run main.py
```

# What's next for First Responder?
Quite a lot, actually. I'm considering what the current state of First Responder is as V2, which is just a complete re-write from V1. This is the MVP, where it just acts as a slightly better job board.

## AI
The issue is I don't want a slightly better job board, I want a **perfect** job board. That's where, you guessed it, AI is going to come into play. From my testing, no matter how many allow and deny filters you set with this scraper, it will not show you only jobs with titles that you'd for sure click on. It will be a lot better than manually going from site to site finding what you want, but it is still not perfect. I believe by using a small LLM (9b, maybe 4b if done locally), the scraper will first only pick job titles that sound like something you would click on (based on a set prompt), but more importantly there will be the ability to find a job based on the title, then view that job posting to see if the description matches what you want. This should, in theory, make it so the **only** jobs sent to Discord will be jobs that you would **actually* apply to.

One issue with this is it uses generative AI, which has lots of ethical complications. My fix to this will be using a small LLM which means it will use significantly less energy and have less impact on the environment than a medium sized model or any of the SOTA models. Originally, I was going to have this fully local, which basically mitigates all ethical concerns, however that would require a computer being on at all times, or using this as an ad-hoc solution, not to constantly see up-to-date jobs. I am looking at using an LLM in V3 of First Responder, and then taking V4 as the version to add the ability to use this in an ad-hoc way, fully local (local LLM, local database).

## Send as text using Twilio
Originally, Discord was not even an option for me as a way to send notifications. What I wanted was to send texts to myself using Twilio anytime it finds a job. I figured out that it would be costly (and more work), so I opted out of it. Now, I'm planning on having the option to either send a long text of links using Twilio rather than on Discord, **or** have the option to maybe recieve a text just saying to check Discord for the new jobs? Not entirely sure yet...!

## Locallization
Most likely not until after the Twilio and LLM implementation of this, but one goal of mine is to make this easy to run locally for ad-hoc job searching. That would mean a local LLM (most likely 4b or even smaller if needed), local database (either SQLite for ease of use, or a Postgres database with Docker), and no option for Twilio texts.