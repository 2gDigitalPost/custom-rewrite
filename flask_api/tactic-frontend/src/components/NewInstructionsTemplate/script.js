/* globals localStorage */

import axios from 'axios'
import marked from 'marked'

export default {
  name: 'NewInstructionsTemplate',
  data () {
    return {
      name: null,
      instructionsText: `# Creating a new Instructions Template
Replace the text here to create the new template. To the right, you can see what the end result will look like.
      
Instruction Templates support Markdown syntax. Here's a few examples of what you can do.
      
# Create several different size headings.
## Using the # symbol at the beginning of your line
### More # symbols will decrease the size of the header

Unordered Lists
* Use a * at the beginning of your line to create an unordered list
* Keep adding asterisks to continue the list
  * Add some space before the asterisk to indent the list

Numbered Lists
1. Or, use a number followed by a period to start a numbered list
2. Use this for lists where the order matters
  3. You can also indent these lists to to start a sub-list
  4. (Numbers revert back to "1" when indenting)
5. But they will resume after the indent.

Surround words with an asterisk to *make them italicized.*

Use two asterisks to **bold something.**`,
    }
  },
  methods: {
    submitToTactic: function() {
      var self = this

      axios.post('/api/v1/instructions-templates', 
        JSON.stringify({
          'name': self.name,
          'instructions_text': self.instructionsText,
          'token': localStorage.tactic_token
        }), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        },
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.$router.push('/instructions-templates/' + response.data.code)
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    update: _.debounce(function (e) {
      this.instructionsText = e.target.value
    }, 300)
  },
  computed: {
    compiledMarkdown: function () {
      return marked(this.instructionsText, { sanitize: true })
    }
  }
}