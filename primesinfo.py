import json
from bisect import bisect_left
from time import time
import logging

import webapp2

from lib.primes import get_all_prime_to_num, get_two_opts

primes = get_all_prime_to_num(999)

class PrimeInfo(webapp2.RequestHandler):
    
    def get(self):
        time_start = time()
        self.response.headers['Content-Type'] = 'application/json'
        num = self.request.get('num')
        try:
            num = int(num)
        except ValueError:
            logging.warn('not acceptable input')
            obj = {'number': num,
                   'prime': '',
                   'Option_1': '',
                   'Option_2': '',
                   'processing_time': ''}
            self.response.out.write(json.dumps(obj))
        else:
            index = bisect_left(primes, num)
            try:
                is_prime = primes[index] == num
            except IndexError:
                is_prime = False
            if not is_prime and num > 20:
                opt1, opt2 = get_two_opts(num, primes)
            processing_time = int((time() - time_start) * 1000)
            obj = {'number': num,
                   'prime': is_prime,
                   'Option_1': '' if is_prime or num <= 20 else '%d + %d + %d = %d' % (opt1 + (num,)) ,
                   'Option_2': '' if is_prime or num <= 20 else '%d + %d + %d = %d' % (opt2 + (num,)) ,
                   'processing_time': processing_time}
            self.response.out.write(json.dumps(obj))

        
application = webapp2.WSGIApplication([
    ('/', PrimeInfo),
], debug=True)
