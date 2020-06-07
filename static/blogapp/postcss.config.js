const purgcss = require("@fullhuman/postcss-purgecss")
const autoprefixer = require("autoprefixer")
const tailwindcss = require("tailwindcss")
const cssnano = require("cssnano")

module.exports = {
    plugins: [
        tailwindcss('./tailwind.config.js'),
        cssnano({
            preset: 'default',
        }),
        purgcss({
            // Specify all paths to your files containing tailwindcss
            content: [],
            extractors: [
                {
                    extractor: class TailwindExtractor {
                        static extract(content) {
                            return content.match(/[A-Z0-9-:\/]+/g) || [];
                        }
                    },
                    extensions: ['css', 'html', 'py']
                }
            ]
        }),
        autoprefixer
    ]
}