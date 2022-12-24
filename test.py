import re

link = '<h1 class="css-swd4zc-TextStyled er34gjf0" data-cy="ad_title">Комнаты для женщин.     Места в женских комнатах.</h1>'
match = re.match(r'''^.*\">(.*)\</.*$''',link)
print (match.group(1))
