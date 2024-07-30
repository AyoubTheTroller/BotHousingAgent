from app.scraping.website.base_loader import BaseLoader
from app.scraping.model.search_params import SearchParams

class UrlBuilder:
    def __init__(self, loader: BaseLoader) -> None:
        self.loader = loader

    def build_url(self, search_params: SearchParams) -> str:
        scheme = self.loader.get_template("scheme")
        host = self.loader.get_template("host")

        # Replace spaces with dashes and convert to lowercase
        formatted_city_name = search_params.location.replace(" ", "-").lower()

        path = self.loader.get_template("paths", "city_rent", city_name=formatted_city_name)
        
        search_params_dict = search_params.model_dump(exclude_unset=True)
        query_string_parts = []

        for param_name, param_value in search_params_dict.items():
            if param_name == "city_name":  # Skip the city as it's part of the path
                continue
            template = self.loader.get_template("query_params", param_name, **{param_name: param_value})
            query_string_parts.append(template)
        
        template = self.loader.get_template("query_params", "order_by_date")
        query_string_parts.append(template)
        
        query_string = "&".join(query_string_parts)
        return f"{scheme}{host}{path}?{query_string}"
