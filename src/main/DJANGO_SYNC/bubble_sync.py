import psycopg2
import json
import sys

DEFAULT_APPROACH = 1

class BubbleMongoSync():
    
    def __init__(self):
        self.con = psycopg2.connect(database='summermiemiepostgre', user='miemie_admin@summermiemie', host='summermiemie.postgres.database.azure.com', password='e_Paswrd?!', port='5432')

    def __progress(self, count: int, total: int, custom_text: str, suffix='') -> None:
        """
            Visualises progress for a process given a current count and a total count
        """

        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))
        percents = round(100.0 * count / float(total), 1)
        bar = '*' * filled_len + '-' * (bar_len - filled_len)
        sys.stdout.write('[%s] %s%s %s %s\r' % (bar, percents, '%', custom_text, suffix))
        sys.stdout.flush()

    def __retrieve_publications(self, limit) -> list:
        cur = self.con.cursor()
        if limit:
            cur.execute('SELECT data, "assignedSDG" FROM public.app_publication LIMIT {}'.format(limit))
        else:
            cur.execute('SELECT data, "assignedSDG" FROM public.app_publication')
        result = cur.fetchall()
        return result

    def __retrieve_approaches(self) -> list:
        cur = self.con.cursor()
        cur.execute('SELECT id, name FROM public.app_approachact')
        result = cur.fetchall()
        return result

    def __retrieve_specialities(self) -> list:
        cur = self.con.cursor()
        cur.execute('SELECT id, name, color_id FROM public.app_specialtyact')
        result = cur.fetchall()
        return result

    def __retrieve_colours(self) -> list:
        cur = self.con.cursor()
        cur.execute('SELECT id, color FROM public.app_coloract')
        result = cur.fetchall()
        return result
    
    def __bubble_exists(self, x, y):
        cur = self.con.cursor()
        query = """SELECT color_id from public.app_bubbleact WHERE coordinate_speciality_id = \'{0}\' AND coordinate_approach_id = \'{1}\'""".format(y, x)
        cur.execute(query)
        return len(cur.fetchall()) != 0

    def __update_bubbles(self, bubble_dict: dict) -> None:
        cur = self.con.cursor()
        c = 1
        l = len(bubble_dict)
        print()
        for i in bubble_dict:
            self.__progress(c, l, "Updating Bubble Chart objects to Postgres")
            if len(bubble_dict[i]['list_of_people']) != 0:
                list_of_ppl = ','.join(bubble_dict[i]['list_of_people'])
                temp = i.replace('(', '').replace(')', '')
                elem = tuple(map(int, temp.split(', ')))

                if not self.__bubble_exists(elem[0], elem[1]):
                    query = "INSERT INTO public.app_bubbleact (coordinate_speciality_id, coordinate_approach_id, color_id, list_of_people) VALUES({0}, {1}, {2}, \'{3}\')".format(elem[1], elem[0], bubble_dict[i]['color'], list_of_ppl)
                else:
                    query = """UPDATE public.app_bubbleact SET coordinate_speciality_id = \'{0}\', coordinate_approach_id = \'{1}\', color_id = \'{2}\', list_of_people = \'{3}\' WHERE coordinate_speciality_id = {0} AND coordinate_approach_id = {1}""".format(
                        elem[1], elem[0], bubble_dict[i]['color'], list_of_ppl)

                cur.execute(query)
                self.con.commit()
            c += 1
        print()

    def __update_userprofiles(self, pubs: dict) -> None:
        cur = self.con.cursor()
        c = 0
        l = len(pubs)

        for pub in pubs:
            author_data = pub[0]['AuthorData']
            link = pub[0]['Link']

            self.__progress(c, l, "Updating app_userprofileact")

            if 'IHE_Prediction' in pub[1] and author_data:
                ihe_prediction = pub[1]['IHE_Prediction']
                for author_id, author_details in author_data.items():
                    name = author_details['Name']
                    affiliation = author_details['AffiliationName']

                    if author_data is not None and author_id is not None and name is not None:
                        if affiliation: affiliation = affiliation.replace("'", "''")
                        if name: name = name.replace("'", "''")
                        
                        
                        cur.execute(
                        """
                            INSERT INTO public.app_userprofileact (\"fullName\", \"scopusLink\", affiliation, author_id) VALUES(\'{0}\', \'{1}\', \'{2}\', {3}) ON CONFLICT (author_id) DO UPDATE SET "fullName" = \'{4}\', "scopusLink" = \'{5}\', affiliation = \'{6}\', author_id = \'{7}\'
                        """.format(name, link, affiliation, author_id, name, link, affiliation, author_id))
                self.con.commit()
            c += 1

    def __create_bubble_data(self, pubs: list) -> dict:
        approach_list = self.__retrieve_approaches()
        specialty_list = self.__retrieve_specialities()
        colors = self.__retrieve_colours()

        new_bubble = {}

        
        for i in approach_list:
            for j in specialty_list:
                new_bubble[str((i[0], j[0]))] = {}
                new_bubble[str((i[0], j[0]))]['color'] = j[2]
                new_bubble[str((i[0], j[0]))]['list_of_people'] = []

        for pub in pubs:
            author_data = pub[0]['AuthorData']
            approach = DEFAULT_APPROACH
            speciality = pub[1]['IHE_Prediction']

            if speciality != '':
                for author_id, author_details in author_data.items():
                    name = author_details['Name']
                    new_bubble[str((approach, int(speciality)))]['list_of_people'].append(author_id)

        self.__update_bubbles(new_bubble)


    def run(self) -> None:
        data_publications  = self.__retrieve_publications(limit=None)
        self.__update_userprofiles(data_publications)
        # self.__create_bubble_data(data_publications)
        self.con.close()
