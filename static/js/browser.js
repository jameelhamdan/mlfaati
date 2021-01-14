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
                    if (!folder.content_length) {
                        folder.size = '';
                    } else {
                        folder.size = humanFileSize(folder.content_length);
                    }

                })
                return list;
            },
            fileList() {
                let list = this.data.files;
                list.forEach(function (file, index) {
                    file.size = humanFileSize(file.content_length);
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
