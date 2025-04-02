# Think Why? News Agent & Instagram Post Optimizer

Hey there! This app does two things:

1. **News Search Engine**: Find news from wherever about whatever.
2. **Instagram Post Optimizer**: Use Google's Gemini AI to make your Insta posts less lame.

## What It Does

### News Search

- Pick a category (Tech, Business, whatever)
- Choose where you want news from
- Decide how fresh you want your news
- Throw in some keywords if you're picky
- Get as many or as few results as you want

### Instagram Post Optimizer

- Paste your mediocre post into the chat thing
- Let AI do its magic
- Get some hashtags (10 max, don't be that person)
- Sound like yourself, just better
- Add those call-to-action things everyone uses
- Make people actually want to read your stuff

## Setting It Up

1. Have Python 3.7+ (duh)

2. Grab the code:
   ```
   git clone https://github.com/sandeep-chakraborty/think-why-agent.git
   cd news-agent
   ```

3. Virtual environment stuff (do it or don't, whatever):
   ```
   python -m venv myenv
   source myenv/bin/activate  # Windows people: myenv\Scripts\activate
   ```

4. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Make a `.env` file with your API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

Need a Gemini API key? Go to [Google AI Studio](https://aistudio.google.com/) and figure it out.

## How to Use It

1. Start it up:
   ```
   streamlit run app.py
   ```

2. It'll open in your browser. If not, go to the URL in the terminal.

3. For news:
   - Pick a category
   - Add keywords if you feel like it
   - Choose a region
   - Pick how old news can be
   - Decide how many results you want

4. Hit "Search News" and boom, articles.

5. Look through the articles, expand them if they seem interesting.

6. Want to post about an article? Click "Create AI Post" and you're golden.

7. In the post generator:
   - Check out what the AI came up with
   - Fix it if it's terrible
   - Copy it
   - Make a new one if you hate it
   - Go back if you regret everything

## Mobile Stuff

Works on your phone too:
- Adjusts to your tiny screen
- Big enough buttons for your thumbs
- Articles that don't make you squint
- Collapsible sections because screen real estate
- Easy to navigate without throwing your phone

## Tech Behind It

- **Streamlit**: Makes the UI not ugly
- **DuckDuckGo Search API**: Free, no auth needed, good enough
- **Gemini API**: The AI that makes your posts better and free
- **Python**: Because obviously

## License

MIT License.