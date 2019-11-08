FROM mediawiki:1.31


RUN git clone --depth 1 -b $MEDIAWIKI_BRANCH \
      https://gerrit.wikimedia.org/r/p/mediawiki/extensions/Babel \
      /var/www/html/extensions/Babel

RUN git clone --depth 1 -b $MEDIAWIKI_BRANCH \
      https://gerrit.wikimedia.org/r/p/mediawiki/extensions/CharInsert \
      /var/www/html/extensions/CharInsert

RUN git clone --depth 1 -b $MEDIAWIKI_BRANCH \
      https://gerrit.wikimedia.org/r/p/mediawiki/extensions/Graph \
      /var/www/html/extensions/Graph

RUN git clone --depth 1 -b $MEDIAWIKI_BRANCH \
      https://gerrit.wikimedia.org/r/p/mediawiki/extensions/Kartographer \
      /var/www/html/extensions/Kartographer

RUN git clone --depth 1 -b $MEDIAWIKI_BRANCH \
      https://gerrit.wikimedia.org/r/p/mediawiki/extensions/LabeledSectionTransclusion \
      /var/www/html/extensions/LabeledSectionTransclusion

RUN git clone --depth 1 -b $MEDIAWIKI_BRANCH \
      https://gerrit.wikimedia.org/r/p/mediawiki/extensions/Math \
      /var/www/html/extensions/Math

RUN git clone --depth 1 -b $MEDIAWIKI_BRANCH \
      https://gerrit.wikimedia.org/r/p/mediawiki/extensions/PageAssessments \
      /var/www/html/extensions/PageAssessments

RUN git clone --depth 1 -b $MEDIAWIKI_BRANCH \
      https://gerrit.wikimedia.org/r/p/mediawiki/extensions/Scribunto \
      /var/www/html/extensions/Scribunto \
      && chmod a+x /var/www/html/extensions/Scribunto/includes/engines/LuaStandalone/binaries/lua*_linux_*/lua

RUN git clone --depth 1 -b $MEDIAWIKI_BRANCH \
      https://gerrit.wikimedia.org/r/p/mediawiki/extensions/TemplateData \
      /var/www/html/extensions/TemplateData

RUN git clone --depth 1 -b $MEDIAWIKI_BRANCH \
      https://gerrit.wikimedia.org/r/p/mediawiki/extensions/TemplateStyles \
      /var/www/html/extensions/TemplateStyles

RUN git clone --depth 1 -b $MEDIAWIKI_BRANCH \
      https://github.com/wikimedia/mediawiki-extensions-wikihiero.git \
      /var/www/html/extensions/WikiHiero

RUN apt-get update && \
      apt-get install -y ploticus fonts-freefont-ttf unzip net-tools nano

RUN git clone --depth 1 -b $MEDIAWIKI_BRANCH \
      https://gerrit.wikimedia.org/r/p/mediawiki/extensions/timeline.git \
      /var/www/html/extensions/timeline \
      && mkdir /var/www/html/images/timeline

RUN git clone --depth 1 -b $MEDIAWIKI_BRANCH \
      https://github.com/wikimedia/mediawiki-extensions-Wikibase.git \
      /var/www/html/extensions/Wikibase \
      && cd /var/www/html/extensions/Wikibase \
      && git submodule update --init --recursive \
      && cd /var/www/html \
      && echo '{ \
  "extra": { \
    "merge-plugin": { \
      "include": [ \
        "extensions/Wikibase/composer.json" \
      ] \
    } \
  } \
}' > composer.local.json \
      && curl -sS https://getcomposer.org/installer -o composer-setup.php \
      && php composer-setup.php --install-dir=/usr/local/bin --filename=composer \
      && rm composer-setup.php \
      && composer install --no-dev

RUN cd extensions/TemplateStyles/ \
      && composer install --no-dev \
      && cd /var/www/html

ADD . /var/www/html

RUN export DOCKER_HOST_IP=$(route -n | awk '/UG[ \t]/{print $2}') \
    && python3 generate_Local_Settings.py "mysql1" "my_wiki" \
    && mv WebRequest.php /var/www/html/includes/ \
    && mv Database.php /var/www/html/includes/libs/rdbms/database/ \
    && mv Parser.php /var/www/html/includes/parser/
