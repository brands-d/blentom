ZIPS = macos linux windows
BUILDDIR = build
TMPDIR = $(BUILDDIR)/tmp
SRCDIR = blentom
VERSION = 3.1.5

.PHONY: all clean

all: clean $(ZIPS)

clean:
	rm -rf $(BUILDDIR)/*.zip $(TMPDIR)

macos:
	rm -rf $(TMPDIR) && mkdir -p $(TMPDIR)/blentom
	rsync -a --exclude='*linux*.whl' --exclude='*win*.whl' $(SRCDIR)/ $(TMPDIR)/blentom/
	cd $(TMPDIR) && zip -r ../blentom-$(VERSION)-macos_arm64.zip blentom
	rm -rf $(TMPDIR)

linux:
	rm -rf $(TMPDIR) && mkdir -p $(TMPDIR)/blentom
	rsync -a --exclude='*mac*.whl' --exclude='*win*.whl' $(SRCDIR)/ $(TMPDIR)/blentom/
	cd $(TMPDIR) && zip -r ../blentom-$(VERSION)-linux_x64.zip blentom
	rm -rf $(TMPDIR)

windows:
	rm -rf $(TMPDIR) && mkdir -p $(TMPDIR)/blentom
	rsync -a --exclude='*mac*.whl' --exclude='*linux*.whl' $(SRCDIR)/ $(TMPDIR)/blentom/
	cd $(TMPDIR) && zip -r ../blentom-$(VERSION)-windows_x64.zip blentom 
	rm -rf $(TMPDIR)