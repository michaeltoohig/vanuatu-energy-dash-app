# Vanuatu Energy Dashboard

An app to display Vanuatu's energy costs and sources as a Dash app.
All data from publicly available sources.

## Development

Run the project locally via Docker

```
# TODO
```

You can then find the app at http://localhost:8050 on your browser.

Or run the project locally without Docker

```
flask --app app.main:app run --reload --debug
```

## Development Notes

TODO:
- [x] refactor loose scripts directory into Click CLI groups
  - [ ] process exchange rate info outside of app; allow app to have a clean static view of what we want to present

- [x] Flatten specific details to single file to simplify stats and other repeated, calculated figures
- [ ] Add context and more explanations around charts
  - [ ] Project renewable usage to 2030
  - [x] Explain latest stat date availability figures
  - [x] Add sources page and links to sources or calculated figures

- [ ] Scrape Unelco's electricity costs breakdowns per month
- [x] Automate fetching WTI records
 
- [ ] Add slider for viewing pie chart of energy sources over time


Stretch Ideas:
- Enter an electricity usage figure and calculate amount at different times in history
- Track power cuts in Port Vila

## Notes

Apparently WTI crude oil price per barrel in USD + 32 USD equals price in VUV (before tax) in 10 weeks.