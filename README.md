# Django00

## Getting Started

Add the following to INSTALLED_APPS in settings:
```
"rest_framework",
"rest_framework.authtoken",
"zerozero",
```

Add to REST_FRAMEWORK in settings:
```
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
}
```

Add to urlpatterns:
```
path("zerozero/api/", include("zerozero.api_urls")),
```

```
pip install -e git+https://gitlab.com/frame-00/00-api.git#zerozero-api
```


## Developer - Getting Started

```
  conda env create -f conda_env.yml
  conda activate zero_zero
  pip install -e ."[dev]"
```

## Testing

  pytest

## Run test App
```
./manage.py migrate
./manage,py runserver
```

## TODO

- Make hypertext serializer only return url if its registered or id if not(so we dont have to add empty resources for each pk)
- Add filter query to list api
- Add fields to csv content type of list api(this might not work)
- Validate order,filter,fields by walking the schema
- Add options request to each resource returning schema information
- Added exclude/include to register so users can block secrets
- Add permissions to register which override the defaults
- Add permissions default setting and use it for all
- Add Reports setting which takes report name, query parameters, and interval.  This creates new endpoints such as .../reports/<slug> which is a CSV
- Create warehousing tasks which run a stored report on a interview and save that into a warehouse or lake(SQL db vs. parquet/csv in s3)
- Create barebones Reports user interace for creating, sharing, and updating them via the website.
