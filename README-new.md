Columns to capture for model
    - user_age
    - venue_country
    - user_type (maybe? do a mosaic plot)
    - 'ticket_type' info (under review)
    - **email_domain**
    - **country**
    - has_analytics
    - count of previous payouts
    - **dummy for org_desc (present/absent)**
    - **dummy for org_name (present/absent)**
    - **T/F for whether 'country' matches 'venue_country'**
    - <name> - MVP+ ?
    - <org_name> - MVP+ ?

5/28 12:00 Next steps
- Review live data to understand pipeline process
- Create a single, featurized data frame for the model
    - One hot encode:
        - 'email_domain' -> 'High Risk e-mail'
        - 'country' -> 'High Risk country'
    - 

- Initial Model
    - Random Forest
    - Boosted
- Subsequent Models
    - XGBoost