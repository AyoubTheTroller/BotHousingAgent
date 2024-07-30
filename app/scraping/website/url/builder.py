from app.scraping.website.base_loader import BaseLoader
from app.scraping.model.search_params import SearchParams

class UrlBuilder:
    def __init__(self, loader: BaseLoader) -> None:
        self.loader = loader
        self.path_keys = self.loader.load_url_template_keys("paths")
        self.query_param_keys = self.loader.load_url_template_keys("query_params")

    def build_url(self, search_params: SearchParams) -> str:
        scheme = self.loader.get_template("scheme")
        host = self.loader.get_template("host")

        # Replace spaces with dashes and convert to lowercase
        formatted_location = search_params.location.replace(" ", "-").lower()
        path_parts = []
        
        search_params_dict = search_params.model_dump(exclude_unset=True)
        query_string_parts = []

        for key in self.path_keys:
            if key == "search_type":
                template = self.loader.get_template("paths",
                                                    "search_type",
                                                    search_params_dict["search_type"],
                                                    location=formatted_location)
                path_parts.append(template)
                continue
            if key in search_params_dict:
                template = self.loader.get_template("paths",key,search_params_dict[key])
                path_parts.append(template)

        for key in self.query_param_keys:
            if key in search_params_dict:
                template = self.loader.get_template("query_params",key,**{key: search_params_dict[key]})
                query_string_parts.append(template)
        
        template = self.loader.get_template("query_params", "order_by_date")
        query_string_parts.append(template)
        
        # Join the path and query string parts
        query_string = "&".join(query_string_parts)
        path = "/".join(path_parts)
        return f"{scheme}{host}/{path}?{query_string}"
