VERSION_SRC := Version.py
VDATE       := $(shell date +'%F %H:%M')


all:
	@echo "done!"




dist:
	git archive --prefix=sanityTool-`cat .version`/ master | bzip2 > sanityTool-`cat .version`.tar.bz2

gittag:
        ifneq ($(TAG),)
	  @git status -s > /tmp/gittag$$$$;                                          \
          if [ -s /tmp/gittag$$$$ ]; then                                            \
	    echo "All files not checked in => try again";                            \
	  else                                                                       \
	    echo $(TAG)                                           >  .version;       \
	    echo 'class Version(object):'                         >> $(VERSION_SRC); \
	    echo '  def __init__(self):'                          >> $(VERSION_SRC); \
            echo '    pass'                                       >> $(VERSION_SRC); \
	    echo '  def tag(self):'                               >> $(VERSION_SRC); \
            echo '    return "$(TAG)"'                            >> $(VERSION_SRC); \
	    echo '  def git(self):'                               >> $(VERSION_SRC); \
            echo '    return "@git@"'                             >> $(VERSION_SRC); \
	    echo '  def date(self):'                              >> $(VERSION_SRC); \
            echo '    return "$(VDATE)"'                          >> $(VERSION_SRC); \
	    echo '  def name(self):'                              >> $(VERSION_SRC); \
            echo '    sA = []'                                    >> $(VERSION_SRC); \
            echo '    sA.append(self.tag())'                      >> $(VERSION_SRC); \
            echo '    sA.append(self.git())'                      >> $(VERSION_SRC); \
            echo '    sA.append(self.date())'                     >> $(VERSION_SRC); \
            echo '    return " ".join(sA)'                        >> $(VERSION_SRC); \
            git commit -m "moving to TAG_VERSION $(TAG)"   .version  $(VERSION_SRC); \
            git tag -a $(TAG) -m 'Setting TAG_VERSION to $(TAG)'                   ; \
	    git push --tags                                                        ; \
          fi;                                                                        \
          rm -f /tmp/gittag$$$$
        else
	  @echo "To git tag do: make gittag TAG=?"
        endif
