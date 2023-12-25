from collections import Counter
import logging
class Vectorize:
    def __init__(self, tokens,text) -> None:
        if not tokens:
            raise ValueError('No tokens found to proceed')
        if not text:
            raise ValueError('No text found in the url')
        self.tokens = tokens
        self.text = text

    def predict(self, n:int,m:int=2):
        '''
        Get the top n topics among both single word and double word combinations.
        args:
            n : number of topics
            m: multiplier factor for the comparision of double word topics. 
            
            eg. if m =2, frequency of each double worded token is taken as twice that of single worded token
        '''
        if m > 5:
            logging.warning(" Keeping a high value of m will skew the topics heavily towards double worded tokens." %m)
        self.topics = []
        self._fit_transform_freqs()
        self._fit_transform_combined_freq(n)
        total_topics = self._get_top_topics(n,m)
        return total_topics
    
    def _fit_transform_freqs(self):
        '''
            Given the tokens and the parsed html content as text, 
            find the frequence-of-occurrences dictionary
            with key as frequency and value as the array of tokens.
        '''

        logging.info('Building the frequency dictionary for single word tokens')
        self.f_d = {}
        self.f= []
        self.counter_f = Counter(self.text.split())
        for w in set(self.tokens):
            freq = self.counter_f[w]
            if not freq: continue
            if '-' in w:
                sub_w = w.split('-')
                for _each in sub_w:
                    if _each.isnumeric() or len(_each)<3: continue
                    freq += self.counter_f[_each]
            self.f_d.setdefault(freq,[]).append(w)

        for freq, value in self.f_d.items():
            self.f.append(freq)
        self.f.sort(reverse=True)
        logging.info('Single token Frequency array obtained %s'%self.f)
        logging.info('Completed.')

    def _fit_transform_combined_freq(self,n):
        '''
            Given the set of single word topics, find popular 2 word
            combinations of topics. 
        '''
        
        logging.info('Building the frequency dictionary for double word tokens')
        self.f2_d = {}
        self.f2 = []
        self.counter_f2 = {}
        single_n_topics = self._get_top_single_topics(n)
        set_topics = set(single_n_topics)
        for w in set_topics:
            temp_set = set(single_n_topics)
            temp_set.remove(w)
            for _comb in temp_set:
                freq = self.text.count(w + ' '+_comb)
                freq_rev = self.text.count(_comb + ' '+w)
                if freq and freq > freq_rev:
                    self.counter_f2.setdefault(w + ' '+ _comb,freq)
                    self.f2_d.setdefault(freq,set()).add(w + ' '+ _comb)
                if freq_rev and freq_rev>freq:
                    self.counter_f2.setdefault(_comb + ' ' +w, freq_rev)
                    self.f2_d.setdefault(freq_rev,set()).add(_comb + ' ' +w)
        
        for freq, value in self.f2_d.items():
            self.f2.append(freq)
        self.f2.sort(reverse=True)
        logging.info('combined token Frequency array obtained %s'%self.f2)
        logging.info('Completed.')

    
    def _get_top_topics(self,n,m):
        '''
            Given the frequency dictionary , get the top n topics based on frequency of single topics
            and combination of topics. For fair comparision, the double word frequency in the corpus is 
            multiplied by factor of m
        '''

        logging.info('Identifying the top %d number of topics ' %n)
        topics = []
        i =0 
        j = 0
        f = self.f
        f2 = self.f2
        count = 0
        while i < len(f) and j < len(f2) and count < n:
            if f[i] < m*f2[j]:
                for w in self.f2_d[f2[j]]:
                    if count < n:
                        topics.append(w)
                        count +=1
                j+=1
            else:
                for w in self.f_d[f[i]]:
                    if count < n:
                        topics.append(w)
                        count +=1
                i+=1
        while count < n and i < len(f):
            for w in self.f_d[f[i]]:
                    if count < n:
                        topics.append(w)
                        count +=1
            i+=1
        while count <n and j < len(f2):
            for w in self.f2_d[f2[j]]:
                    if count < n:
                        topics.append(w)
                        count +=1
            j+=1
        
        if count==n:
            logging.info('Found the top %d topics'%n)
        else:
            logging.info('Could not find %d topics instead found %d topics'%(count,n))
        return topics
    
    def _get_top_single_topics(self,n:int):
        count = 0
        single_n_topics = []
        for freq in self.f:
            for w in self.f_d[freq]:
                if count ==n:break
                single_n_topics.append(w)
                count +=1
            if count == n: break
        return single_n_topics