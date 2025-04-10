# !pip install geopy
# !pip install pandas

# Colab Case
# for fn in uploaded.keys():
#   print('User uploaded file "{name}" with length {length} bytes'.format(
#       name=fn, length=len(uploaded[fn])))
# df = pd.read_csv(io.BytesIO(uploaded[fn]), encoding='cp949')

file_path = '/content/drive/MyDrive/your_file.csv'
df = pd.read_csv(file_path, encoding='cp949')

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def calculate_distance(location1, location2):
    geolocator = Nominatim(user_agent="geoapi_example")

    def get_coordinates(location):
        if isinstance(location, str):  
            try:
                location = geolocator.geocode(location)
                if location:
                    return location.latitude, location.longitude
                else:
                    return None
            except Exception as e:
                return None
        elif isinstance(location, tuple) and len(location) == 2: 
            return location
        else:
            return None

    coord1 = get_coordinates(location1)
    coord2 = get_coordinates(location2)

    if coord1 is None or coord2 is None:
        return "위치 정보를 찾을 수 없습니다."

    distance_km = geodesic(coord1, coord2).kilometers
    return distance_km


if __name__ == "__main__":
    address1 = "서울특별시 중구 세종대로 110"
    for index, row in df.iterrows():
        latitude = row['위도']
        longitude = row['경도']
        try:
            print(calculate_distance((latitude, longitude), address1))
        except:
            pass
        break
