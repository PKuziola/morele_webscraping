<a name="readme-top"></a>
# 👨‍💻 Built with
<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" /> <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white"/> 
<img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white"/>
<img src="https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white"/>
<img src="https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white"/>
<img src="https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white"/>

<!-- ABOUT THE PROJECT -->
# About The Project

![morele_img][morele-url]


This project job is to:<p>
- webscrap data from [Morele.net](https://www.morele.net/kategoria/karty-graficzne-12/) store<p>
    We achieve this by running scrapy spider which crawls through every card's webpage to obtain all possible data<p>
- visualize data <p>
    Projects creates .ipynb file which connects to database to provide insight into graphic cards available in [Morele.net](https://www.morele.net/kategoria/karty-graficzne-12/) store through the visualization of data scraped from [Morele.net](https://www.morele.net/kategoria/karty-graficzne-12/)<p>
- build model <p>
    In order to predict card price XGBoost model was developed, measures such as hyperparameter tuning, variable's categorization, outlier removal were undertaken to achieve best possible model performance <p>
- give recommendation<p>
    Based on developed model I listed the best cards you can buy under certain price thresholds. I believe these cards provide best value-for-money. <p>

### Recommendation example - Top 5 Cards under 2000 zł budget

<img src="https://raw.githubusercontent.com/PKuziola/morele_webscraping/main/img/img_1.png"/>


# Database consists of one table

### graphic_cards

| Column_name  | Datatype | Description |
| ------------- | ------------- | ------------- |
| ean  | VARCHAR(15)  | European Article Number | 
| dlss_3_0  | VARCHAR(10)  | Information whether graphic cards has Deep Learning Super Sampling technology    |
| d_sub  | VARCHAR(10)  | Number of D-Sub ports  |
| display_port  | VARCHAR(10)  | Number of DisplayPorts ports  |
| mini_display_port  | VARCHAR(10)  | Number of Mini DisplayPorts ports  |
| dvi  | VARCHAR(10)  | Number of DVI ports  |
| hdmi  | VARCHAR(10)  | Number of HDMI ports  |
| usb_c  | VARCHAR(10)  | Number of USB-C ports  |
| card_name  | TEXT  | Graphic card's name  |
| card_id  | VARCHAR(25)  | Graphic card's ID  |
| card_price  | FLOAT(2)  | Graphic card's price [zł]  |
| stock  | INT  | Amount of graphic cards available  |
| rating_count  | INT  | Number of ratings  |
| questions  | INT  | Number of questions asked  |
| buyers  | INT  | Amount of card sold  |
| rating  | FLOAT(2)  | Rating  |
| card_manufacturer  | TEXT  | Card manufacturer  |
| card_manufacturer_code  | VARCHAR(70)  | Card's manufacturer code  |
| chipset_brand  | TEXT  | Chipset manufacturer  |
| chipset_type  | TEXT  | Chipset type  |
| clock_speed  | VARCHAR(11)  | Clock speed [Mhz]  |
| clock_speed_boost_mode  | VARCHAR(11)  | Clock speed in boost mode [Mhz]  |
| stream_processors  | INT  | Number of stream processors  |
| rop_units  | INT  | Number of ROP units  |
| texturing_units  | INT  | Number of texturing units  |
| rt_cores  | INT  | Number of RT Cores  |
| tensor_cores  | INT  | Number of Tensor Cores  |
| connector_type  | VARCHAR(25)  | Connector Type  |
| card_length  | INT  | Graphic card's length [mm]  |
| card_linking | TEXT  | Information whether there is option to link cards |
| card_resolution  | VARCHAR(25)  | Graphic card's resolution  |
| recommended_power_supply_wattage  | INT  | Graphic card's recommended power supply [W]  |
| led_backlighting  | VARCHAR(25)  | Information whether graphic cards has led backlighting  |
| ram_capacity | INT  | RAM Capacity [GB]  |
| ram_type | VARCHAR(25)  | RAM Type  |
| data_bus | VARCHAR(25)  | station's city [bit]  |
| memory_clock | INT  | Memory clocking [Mhz]  |
| cooling_type | VARCHAR(25)  | Graphic card's cooling type  |
| fans_quantity | INT  | Number of fans  |
| power_ports | VARCHAR(25)  | Number and type of power connectors  |
| packaging_version | TEXT  | Information how is graphic card boxed  |



<p align="right">(<a href="#readme-top">back to top</a>)</p>


# 🔑Setup

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Getting Started

```bash
# Clone the repository
$ git clone https://github.com/PKuziola/morele_webscraping.git
# Navigate to the project folder
$ cd morele_webscraping
# Remove the original remote repository
$ git remote remove origin
```

### Setuping local variables

Before running project you need to assign environmental variables .env file.

```bash
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
```

### Building container

Run dockercomposer:
```bash
docker compose up --build .
```


<p align="right">(<a href="#readme-top">back to top</a>)</p>

# 🌲 Project tree
```bash
.
├───database
│   ├───Dockerfile
│   ├───init.sql
├───img
│   └──img_1.png
├───morele
│   ├── morele
│   │   ├── __init__.py
│   │   ├── items.py
│   │   ├── middlewares.py
│   │   ├── pipelines.py
│   │   ├── settings.py
│   │   └── spiders
│   │        ├── __init__.py
│   │        └── morele_spider.py
│   ├── Dockerfile
│   └── requirements.txt
├───notebook
│   ├───data_analysis_pc.ipynb
│   └──Dockerfile
├── docker-compose.yaml
├── license.txt
├── README.md 
└── .env - sample

```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
# 📄 License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[morele]: https://www.morele.net/kategoria/karty-graficzne-12/
[morele-url]: https://www.morele.net/static/img/shop/logo/image-logo-morele.svg
[linkedin-shield]: https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white
[linkedin-url]: https://www.linkedin.com/in/piotr-kuzio%C5%82a-992b00174/
[product-screenshot]: images/screenshot.png


