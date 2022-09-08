import re


class LogParcer:
    def parce(self, text: str):
        url = self._get_url(text)
        time = self._get_time(text)

        return url, time

    def _get_url(self, text: str):
        pattern = r'(?:GET|POST|PUT|DELETE|PATCH|OPTIONS) /\S*'
        match = re.search(pattern, text)
        if match:
            url = match[0].split(' ')
            return url[-1]

        return None

    def _get_time(self, text: str):
        text_list = text.split(' ')
        request_time = text_list[-1].strip()
        if request_time.replace('.', '').isdigit():
            return float(request_time)

        return None
