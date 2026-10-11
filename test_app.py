import subprocess,time,os,json,sys
from playwright.sync_api import sync_playwright
root=os.path.dirname(__file__)
html=open(os.path.join(root,'index.html')).read()
fail=[]
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
  page=browser.new_page(viewport={'width':1440,'height':900},device_scale_factor=1)
  errors=[];page.on('pageerror',lambda e: errors.append(str(e)))
  page.evaluate('''() => {const mem={}; Object.defineProperty(window,'localStorage',{value:{getItem:k=>mem[k]||null,setItem:(k,v)=>mem[k]=String(v),removeItem:k=>delete mem[k]}})}''')
  page.set_content(html,wait_until='domcontentloaded')
  page.wait_for_timeout(700)
  print('title',page.title(),'rendered',page.locator('#stats .stat-card').count())
  assert page.locator('#stats .stat-card').count()==4
  page.screenshot(path='/mnt/data/CareerDisha_AI_Desktop_Preview.png',full_page=True)
  # roadmap interaction
  page.locator('#desktopNav [data-nav="roadmap"]').click()
  assert page.locator('#view-roadmap.active').count()==1
  assert page.locator('#roadmapTimeline .timeline-item').count()==4
  page.locator('#roadHours').fill('10')
  page.locator('#generateBtn').click()
  assert page.locator('#roadmapEstimate').inner_text().find('10 hrs')!=-1
  page.locator('#roadmapTimeline [data-toggle-task]').first.click()
  assert '✓' in page.locator('#roadmapTimeline [data-toggle-task]').first.inner_text()
  page.locator('#desktopNav [data-nav="dashboard"]').click()
  assert page.locator('#ringLabel').inner_text()=='13%'
  # jobs tests
  page.locator('#desktopNav [data-nav="jobs"]').click()
  page.locator('button[data-sample="python"]').click()
  page.locator('#analyzeBtn').click()
  print('job comparison',page.locator('#jobResultCard').inner_text()[:420])
  assert page.locator('#jobResultCard').get_by_text('Potential gaps').count()==1
  assert 'Flask' in page.locator('#jobResultCard').inner_text()
  page.locator('#addGapsBtn').click()
  assert page.locator('#view-roadmap.active').count()==1
  assert page.locator('#roadmapTimeline .timeline-item').count()==5
  # resources
  page.locator('#desktopNav [data-nav="resources"]').click()
  assert page.locator('.resource-card').count()>=8
  # offline chat
  page.locator('#desktopNav [data-nav="coach"]').click()
  page.locator('#chatInput').fill('What should I learn next?')
  page.locator('#chatForm button[type="submit"]').click()
  page.wait_for_timeout(300)
  assert page.locator('.bubble.bot').count()>=1
  # profile save
  page.locator('.sidebar [data-nav="profile"]').click()
  page.locator('#profileName').fill('Test Student')
  page.locator('#saveProfileBtn').click()
  assert page.locator('#sideName').inner_text()=='Test Student'
  page.set_content(html,wait_until='domcontentloaded');page.wait_for_timeout(100)
  assert page.locator('#sideName').inner_text()=='Test Student'
  assert page.locator('#ringLabel').inner_text()=='8%' # 1 completed of 13 tracked tasks
  print('persist works, progress=',page.locator('#ringLabel').inner_text())
  page.locator('.sidebar [data-nav="profile"]').click()
  print('export UI visible',page.locator('#exportBtn').is_visible(),flush=True)
  # mobile
  mobile=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1,is_mobile=True,has_touch=True)
  mobile_errors=[];mobile.on('pageerror',lambda e:mobile_errors.append(str(e)))
  mobile.set_content(html,wait_until='domcontentloaded');mobile.wait_for_timeout(300)
  mobile.screenshot(path='/mnt/data/CareerDisha_AI_Mobile_Preview.png',full_page=True)
  assert mobile.locator('.bottomnav').is_visible()
  mobile.locator('#mobileNav [data-nav="roadmap"]').click()
  assert mobile.locator('#view-roadmap.active').count()==1
  mobile.screenshot(path='/mnt/data/CareerDisha_AI_Roadmap_Mobile.png',full_page=True)
  mobile.locator('#mobileNav [data-nav="jobs"]').click()
  mobile.locator('button[data-sample="data"]').click()
  mobile.locator('#analyzeBtn').click()
  mobile.screenshot(path='/mnt/data/CareerDisha_AI_Job_Analyzer_Mobile.png',full_page=True)
  assert 'Data Visualization' in mobile.locator('#jobResultCard').inner_text()
  print('mobile overflow',mobile.evaluate('document.documentElement.scrollWidth - window.innerWidth'))
  print('desktop errors',errors,'mobile errors',mobile_errors)
  assert not errors and not mobile_errors
  assert mobile.evaluate('document.documentElement.scrollWidth - window.innerWidth')<=2
  browser.close()
finally:
 pass