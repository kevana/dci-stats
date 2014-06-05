'''Main entry point.'''


from bs4 import BeautifulSoup
from collections import Counter
import operator
from pprint import pprint


testData = '''
<div class='author_info'>
                <div itemscope itemtype="http://schema.org/Person" class='user_details'>
    <span class='hide' itemprop="name">perc2100</span>
    <ul class='basic_info'>     
            <p class='desc member_title'>DCP Fanatic</p>
        <li class='avatar'>     
                    <img itemprop="image" src='http://www.drumcorpsplanet.com/forums/uploads/av-500.jpg?_r=0' class='ipsUserPhoto ipsUserPhoto_large' />                
            </li>
        <li class='group_title'>
            Members
        </li>
        <li class='group_icon'>
                <img src='http://www.drumcorpsplanet.com/forums/public/style_images/master/bullet_black.png' alt='Pip' /><img src='http://www.drumcorpsplanet.com/forums/public/style_images/master/bullet_black.png' alt='Pip' /><img src='http://www.drumcorpsplanet.com/forums/public/style_images/master/bullet_black.png' alt='Pip' /><img src='http://www.drumcorpsplanet.com/forums/public/style_images/master/bullet_black.png' alt='Pip' /><img src='http://www.drumcorpsplanet.com/forums/public/style_images/master/bullet_black.png' alt='Pip' />
            </li>
        <li class='post_count desc lighter'>
            6,515 posts
        </li>
    </ul>
        <ul class='custom_fields'>   
        </ul>
</div>
            </div>
            <div class='post_body'>
                <p class='posted_info desc lighter ipsType_small'>
                    Posted <abbr class="published" itemprop="commentTime" title="2013-08-11T03:47:28+00:00">10 August 2013 - 10:47 PM</abbr>  
                </p>
                <div itemprop="commentText" class='post entry-content '>
                    <!--cached-Sat, 31 May 2014 03:44:21 +0000-->So, who&#39;s going to take it all next year?&#33;
                    <br />
                </div>
                <div class='ipsLikeBar right clearfix' id='rep_post_3309068'>
                <ul class='ipsList_inline'>
                </ul>
            </div>
'''

with open('2014_Predictions.html', encoding='iso-8859-1') as page:
    data = page.read()

    soup = BeautifulSoup(data)
    # Remove script and style tags
    [s.extract() for s in soup(['script', 'style'])]

    posts = [post.get_text() for post in soup.find_all('div', class_='post_body')]
    # print(posts)

    cnt = Counter()
    for post in posts:
        for word in post.split():
            if word.lower() in ['bluecoats', 'devils', 'crown', 'caveliers',
                                'phantom', 'scv', 'stars', 'cadets']:
                cnt[word.lower()] += 1

    sorted_cnt = sorted(cnt.items(),
                        key=operator.itemgetter(1),
                        reverse=True)
    print('========= Results ===========')
    pprint(sorted_cnt[:30])
