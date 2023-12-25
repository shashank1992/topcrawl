import sys
from absl import app
from absl import flags
import logging

flags.DEFINE_string('url','','The url entered as string to parse the html')
flags.DEFINE_integer('n',10,'The total number of topics to receive. Type integer', lower_bound=0)
flags.DEFINE_integer('m',2,'The multiplier factor for double-word topic combinations to compare against single-word',lower_bound=0)

FLAGS = flags.FLAGS
FLAGS(sys.argv)

def main(argv):
    url = FLAGS.url
    n = FLAGS.n
    m = FLAGS.m
    if not url:
        logging.warning('Did not receive any url')
        url = input('Please enter the url to proceed \n')

    from topics import Topics as topics

    try:
        ans = topics(url).get_topics(n,m)
        logging.info('The obtained %d topics for this webpage are %s'%(n,ans))
    except Exception as e:
        logging.info('Terminating due to error %s'%e)
if __name__=="__main__":
    app.run(main)