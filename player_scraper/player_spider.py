import scrapy


class PlayerSpider(scrapy.Spider):
    name = "Player"
    baseurl = 'https://fbref.com'
    #start_urls= ['https://fbref.com/en/players/6025fab1/dom_lg']

    # Comment this function and uncomment start_urls to test for one player
    def start_requests(self):
        yield scrapy.Request(url = self.baseurl+'/en/comps', callback=self.getleagueurl)

    def getleagueurl(self , response):
        url=self.scrapeurl('La Liga',response)
        yield scrapy.Request(url=self.baseurl+url , callback=self.getseasonurl)

    def getseasonurl(self , response ):
        url=self.scrapeurl('2020-2021',response)
        yield scrapy.Request(url=self.baseurl+url , callback=self.getteamurls)

    def scrapeurl(self ,s,response):
        comps_tables = response.css('table')
        for a in comps_tables:
            for b in a.css('a'):
                if b.css('a::text').get()==s:
                    return b.css('a::attr(href)').get()

    def getteamurls(self , response):
        self.log("Reached team urls")
        self.log(response.url)
        td = response.css('table')[0].css('td[data-stat="squad"]')
        for i in td:
            a=i.css('a::attr(href)')
            yield response.follow(a.get(), callback=self.getplayerurl)

    def getplayerurl(self , response):
        
        self.log(response.url)
        th = response.css('table')[0].css('th[data-stat="player"][scope="row"]')
        for i in th:
            a = i.css('a::attr(href)')
            url=a.get()
            if(url=="" or url==None):
                continue
            # self.log("url="+url)
            yield response.follow(url, callback=self.parse)
    


    
    # This is the main function that scrapes the player data
    def parse(self , response):
        playerdata={}

        playerdata['name']=response.css('h1[itemprop="name"] span').css('span::text').get()

        table_ids = ['#div_stats_standard_dom_lg tbody', '#div_stats_shooting_dom_lg tbody', '#div_stats_passing_dom_lg tbody', '#div_stats_gca_dom_lg tbody', '#div_stats_defense_dom_lg tbody', '#div_stats_possession_dom_lg tbody', '#div_stats_misc_dom_lg tbody']


        features=[['goals_per90','assists_per90','goals_assists_pens_per90', 'goals_pens_per90', 'goals_assists_pens_per90'], ['goals','shots_total_per90', 'shots_on_target_per90', 'shots_free_kicks', 'pens_made'], ['passes_completed','passes','passes_completed_short','passes_completed_medium','passes_completed_long'],['sca','sca_per90','gca_per90'],['tackles', 'tackles_won', 'dribbles_vs', 'pressures', 'pressure_regains', 'blocks', 'blocked_shots'], ['dribbles_completed', 'carry_distance'], ['fouls','aerials_won', 'ball_recoveries']]

        # Total 7 tables in the page scrapping from
        for i in range(7):
            # Get standard stat table using its identifier
            standard_stats=self.getlast3seasonrows(response , table_ids[i] )

            # Puts the feature and their value in player data object
            self.getfeaturevals( standard_stats , features[i] ,playerdata)
        
        ############# more tables here


        yield playerdata

    
    # Helper functions for parse function
    def getfeaturevals(self,table , features , playerdata):
        for feature in features:
            playerdata[feature]=[]
            for row in table:
                val=row.css('td[data-stat="{0}"]'.format(feature)).css('td::text').get()
                # val=float(val)
                playerdata[feature].append(val)


    def getlast3seasonrows(self,response , id):
        # Get  stat table using its identifier
        stat_table=response.css(id)
        # self.log(stat_table.get())
        # self.log(response.css('body').get())
        rows=stat_table.css('tr')

        if len(rows) < 3:
            return rows
        #Getting last 3 rows
        return rows[-3:]
