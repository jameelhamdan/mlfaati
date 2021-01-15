{
    Vue.createApp({
        delimiters: ['[[', ']]'],
        data() {
            return {
                loading: true,
                rootApiUrl: rootApiUrl,
                data: {
                    current_folder: null,
                    folders: [],
                    files: [],
                }
            }
        },
        computed: {
            currentFolder() {
                let current = this.data.current_folder;
                if (!current) return null;

                if (current.ancestors.length > 0) {
                    current.previous = current.ancestors[current.ancestors.length - 1];
                } else {
                    current.previous = null;
                }
                return current
            },
            folderList() {
                let list = this.data.folders;
                list.forEach(function (folder, index) {
                    folder.created_on_display = moment(folder.created_on).fromNow();
                    folder.updated_on_display = moment(folder.updated_on).fromNow();
                    folder.size = folder.content_length ? humanFileSize(folder.content_length) : '';
                })
                return list;
            },
            fileList() {
                let list = this.data.files;
                list.forEach(function (file, index) {
                    file.created_on_display = moment(file.created_on).fromNow();
                    file.updated_on_display = moment(file.updated_on).fromNow();
                    file.size = humanFileSize(file.content_length);

                    list.forEach(function (childFile, index) {
                        childFile.created_on_display = moment(childFile.created_on).fromNow();
                        childFile.updated_on_display = moment(childFile.updated_on).fromNow();
                        childFile.size = humanFileSize(childFile.content_length);
                    });
                })
                return list;
            },
        },
        created() {
            this.loadData(this.rootApiUrl);
        },
        methods: {
            openFile(file) {
                window.open(file.serve_url, '_blank').focus();
            },
            openFolder(folder = null) {
                if (folder) {
                    this.loadData(folder.url);
                } else {
                    this.loadData(this.rootApiUrl);
                }
            },
            loadData(url) {
                let $this = this;
                $this.loading = true;
                axios.get(url).then(res => {
                    $this.data = res.data;
                    $this.loading = false;
                });
            },
        }
    }).mount('#browserApp');
}
