# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import time

opts = ChromeOptions()
opts.add_argument("--window-size=2560,1440") 

class Admin (unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(options=opts)
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_admin(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")

        # Login
        print("******************************TEST LOGIN************************************************************")
        driver.save_screenshot("screenshot/E-Commerce-Home.png")
        driver.find_element(By.LINK_TEXT,"Getting Started").click()
        driver.find_element(By.ID,"username").click()
        driver.find_element(By.ID,"username").clear()
        driver.find_element(By.ID,"username").send_keys("admin")
        driver.find_element(By.ID,"password").click()
        driver.find_element(By.ID,"password").clear()
        driver.find_element(By.ID,"password").send_keys("admin")
        driver.save_screenshot("screenshot/E-Commerce-Login.png")
        driver.find_element(By.ID,"submit").click()
        driver.save_screenshot("screenshot/E-Commerce-Adminpanel.png")

        #Test
        message_Login = driver.find_element(By.XPATH,"//div[@class='alert alert-success'][1]").text
        message_attendu1 = "×\nSuccess! You are logged in as: admin"
        self.assertEqual(message_Login, message_attendu1)
        print(f'test login passed')

        #Delete user
        print("******************************DELETE USER************************************************************")
        user_list_initial = driver.find_elements(By.XPATH,"//div/div[2]/table/tbody/tr/td[1]")
        user_number = len(user_list_initial) 
        print(f'la nombre des utilisateurs initial est {user_number}')

        driver.find_element(By.XPATH,"(.//*[normalize-space(text()) and normalize-space(.)='Empty'])[2]/following::button[1]").click()
        driver.save_screenshot("screenshot/E-Commerce-DeleteUser.png")

        if user_number == 3 :
            print("test delete user failed")
        else :
            print("test delete user passed")

        #Consulter les bugets 
        print("******************************CONSULTER LES BUDGETS************************************************************")    
        #ADMIN
        admin_budget = driver.find_element(By.XPATH,"//div[@class='col-4'][1]/table[@class='table table-hover table-dark'][1]/tbody[1]/tr[1]/td[3]").text
        driver.save_screenshot("screenshot/E-Commerce-AdminBudget.png")
        resultat_trouvé =  float(''.join(filter(str.isdigit, admin_budget)))
        print(resultat_trouvé)
        resulat_attendus = 0.0
        if resultat_trouvé == resulat_attendus :
            print(f'le directeur nest pas autorisé à disposer d un budget, test passed')
        else :
            print("test failed")
        
        #USERS
        user1_budget = driver.find_element(By.XPATH,"//div[@class='col-4'][1]/table[@class='table table-hover table-dark'][1]/tbody[1]/tr[2]/td[3]").text
        driver.save_screenshot("screenshot/E-Commerce-UserBudget.png")
        resultat_user1_budget =  float(''.join(filter(str.isdigit, user1_budget)))
        budget_max = 10000
        self.assertGreaterEqual(budget_max, resultat_user1_budget)
        print(f'le budget maximum d un utilisateur est 10.000 $, test passed')

        user2_budget = driver.find_element(By.XPATH,"//div[@class='col-4'][1]/table[@class='table table-hover table-dark'][1]/tbody[1]/tr[3]/td[3]").text
        resultat_user2_budget =  float(''.join(filter(str.isdigit, user2_budget)))
        self.assertGreaterEqual(budget_max, resultat_user2_budget)
        print(f'le budget maximum d un utilisateur est 10.000 $, test passed')



        #Gérer les commandes 
        print("******************************GERER LES COMMANDS************************************************************")
        list_commandes = driver.find_elements(By.XPATH,"//div/div[2]/table[@class='table table-hover table-dark']/tbody/tr")
        driver.save_screenshot("screenshot/E-Commerce-LesCommandes.png")
        
        print("la liste des commandes:")
        for row in list_commandes:
            cells = row.find_elements(By.TAG_NAME, "td")

            row_text = ""
            for cell in cells :
                row_text += cell.text + "\t"
            print(row_text)


        #Supprimer un article 
        print("******************************DELETE ITEMS************************************************************")
        list_article = driver.find_elements(By.XPATH,"//div/div[1]/table/tbody/tr/td[1]")
        nombre_article = len(list_article)
        print(f'le nombre d article {nombre_article}')

        driver.find_element(By.XPATH,"(.//*[normalize-space(text()) and normalize-space(.)='Update'])[1]/following::button[1]").click()
        driver.save_screenshot("screenshot/E-Commerce-DeleteIPhone15.png")
        driver.find_element(By.XPATH,"(.//*[normalize-space(text()) and normalize-space(.)='Update'])[3]/following::button[1]").click()
        driver.save_screenshot("screenshot/E-Commerce-DeleteGalaxyZFold.png")
        driver.find_element(By.XPATH,"(.//*[normalize-space(text()) and normalize-space(.)='Update'])[10]/following::button[1]").click()
        driver.save_screenshot("screenshot/E-Commerce-DeleteDellXPS13Laptop.png")
        driver.find_element(By.XPATH,"(.//*[normalize-space(text()) and normalize-space(.)='Update'])[20]/following::button[1]").click()
        driver.save_screenshot("screenshot/E-Commerce-DeleteHPEnvyx360Laptop.png")

        if nombre_article != 20 :
            print("test delete item passed")
        else :
            print("test delete item failed")


        #Verifier 
        print("******************************VERIFICATION LE NOM ET LE PRIX D UN ARTICLE************************************************************")
        article_rechercher = "IPhone 15"

        list_article_name = driver.find_elements(By.XPATH,"div/div[1]/table/tbody/tr/td[2]")
        article_trouvé = False
        for name in list_article_name:
            if article_rechercher in name.text :
                article_trouvé = True
                break
        
        if article_trouvé :
            print(f'test failed')
        else :
            print(f'there is IPhone 15 in the list, test passed')


        price_of_MacBook_Air = driver.find_element(By.XPATH,"//div/div[1]/table/tbody/tr[2]/td[3]").text
        resultat_trouvé2 =  float(''.join(filter(str.isdigit, price_of_MacBook_Air)))
        print(resultat_trouvé2)
        resulat_attendus2 = 8500.0
        self.assertEqual(resultat_trouvé2, resulat_attendus2)
        print(f'le prix d un MacBook_Air est {resulat_attendus2}, test passed ')




        #Mettre à jour un article 
        print("******************************UPDATE ITEM************************************************************")
        driver.find_element(By.XPATH,"(.//*[normalize-space(text()) and normalize-space(.)='IPhone 15'])[1]/following::button[1]").click()
        driver.save_screenshot("screenshot/E-Commerce-UpdateIphone15.png")
        driver.find_element(By.XPATH,"(.//*[normalize-space(text()) and normalize-space(.)='Galaxy Z Fold'])[1]/following::button[1]").click()
        driver.save_screenshot("screenshot/E-Commerce-UpdateGalaxyZflod.png")
        driver.find_element(By.XPATH,"(.//*[normalize-space(text()) and normalize-space(.)='Dell XPS 13 Laptop'])[1]/following::button[1]").click()
        driver.save_screenshot("screenshot/E-Commerce-UpdateDellXPS13Laptop.png")
        

        #Acheter des articles 
        print("******************************BUY ITEM************************************************************")
        driver.find_element(By.LINK_TEXT,"Market").click()
        driver.find_element(By.XPATH,"(.//*[normalize-space(text()) and normalize-space(.)='Info'])[3]/following::button[1]").click()
        driver.find_element(By.XPATH,"//div[@id='Buy-3']/div/div/div[2]/div/input[2]").click()
        driver.save_screenshot("screenshot/E-Commerce-BuyGalaxy-Z-Fold.png")

        message_erreur = driver.find_element(By.XPATH,"//div[@class='alert alert-danger'][1]").text
        message_attendu3 = "×\nUnfortunately, you don't have enough money to purchase Galaxy Z Fold!" 
        self.assertEqual(message_erreur, message_attendu3)
        print(f'test buy of Galaxy Z Fold passed')

        driver.find_element(By.XPATH,"(.//*[normalize-space(text()) and normalize-space(.)='Info'])[1]/following::button[1]").click()
        driver.find_element(By.ID,"submit").click()

        driver.save_screenshot("screenshot/E-Commerce-BuyIPhone 15.png")
        message_erreur1 = driver.find_element(By.XPATH,"//div[@class='alert alert-danger'][1]").text
        message_attendu4 = "×\nUnfortunately, you don't have enough money to purchase IPhone 15!" 
        self.assertEqual(message_erreur1, message_attendu4)
        print(f'test buy of IPhone 15 passed')


        #Logout
        print("******************************LOGOUT************************************************************")
        driver.find_element(By.LINK_TEXT,"Logout").click()
        driver.save_screenshot("screenshot/E-Commerce-Logout.png")

        message_Logout = driver.find_element(By.XPATH,"//div[@class='alert alert-info'][1]").text
        message_attendu2 = "×\nYou have been logged out!"
        self.assertEqual(message_Logout, message_attendu2)
        print(f'test logout passed')

        driver.get("http://127.0.0.1:5000/")

        #Afficher les détails
        print("******************************AFFICHER LE DETAILS D UN ARTICLE ************************************************************")
        driver.get("http://127.0.0.1:5000/")
        driver.find_element(By.LINK_TEXT,"Getting Started").click()
        driver.find_element(By.ID,"username").click()
        driver.find_element(By.ID,"username").clear()
        driver.find_element(By.ID,"username").send_keys("admin")
        driver.find_element(By.ID,"password").click()
        driver.find_element(By.ID,"password").clear()
        driver.find_element(By.ID,"password").send_keys("admin")
        driver.find_element(By.ID,"submit").click()
        driver.find_element(By.LINK_TEXT,"Market").click()
        driver.find_element(By.XPATH,"(.//*[normalize-space(text()) and normalize-space(.)='IPhone 15'])[4]/following::button[1]").click()
        driver.find_element(By.XPATH,"//div/div/div/div[3]/button").click()
        driver.save_screenshot("screenshot/E-Commerce-Info.png")

        item_name = driver.find_element(By.XPATH,"//h5[@id='ModalLabel'][1]/strong[1]").text 
        les_infos = driver.find_element(By.XPATH,"//div/div/div/div[2]").text
        print(f'les infos de {item_name} sont: {les_infos}')

        driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[1]/div/div/div[3]/button")

       



    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()


       