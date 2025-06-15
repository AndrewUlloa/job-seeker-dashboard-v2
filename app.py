#!/usr/bin/env python3
"""
Fast Job Seeker Dashboard for Cap-Exempt H-1B Employers
Optimized for instant loading and HF Spaces deployment
"""

import gradio as gr
import pandas as pd
import plotly.express as px
import os
import numpy as np
import time
from typing import List, Tuple

class FastJobSeekerDashboard:
    def __init__(self):
        self.data = None
        self.load_data_fast()
        
    def load_data_fast(self):
        """Fast data loading with multi-year support."""
        print("🚀 Loading data from both 2024 and 2025 sources...")
        
        # Define data sources with years
        data_sources = [
            {'file': 'optimized_employers.parquet', 'year': '2024', 'limit': None},
            {'file': 'optimized_employers.csv', 'year': '2024', 'limit': None},
            {'file': 'LCA_2025_dashboard_ready.csv', 'year': '2025', 'limit': None},
            {'file': 'likely_cap_exempt_employers.csv', 'year': '2024', 'limit': None},
            {'file': 'cap_exempt_analysis_results.csv', 'year': '2024', 'limit': None}
        ]
        
        combined_data = []
        loaded_years = set()
        
        for source in data_sources:
            filename = source['file']
            year = source['year']
            limit = source['limit']
            
            if os.path.exists(filename):
                try:
                    print(f"📊 Loading {year} data from {filename}...")
                    
                    # Load data
                    if filename.endswith('.parquet'):
                        df = pd.read_parquet(filename)
                    else:
                        if limit is not None:
                            df = pd.read_csv(filename, nrows=limit)
                        else:
                            df = pd.read_csv(filename)
                    
                    # Add/fix year column
                    df['Data_Year'] = year
                    
                    # Standardize required columns
                    required_cols = ['Employer_Name', 'State', 'Data_Year']
                    if all(col in df.columns for col in required_cols):
                        combined_data.append(df)
                        loaded_years.add(year)
                        print(f"✅ Loaded {len(df):,} records from {year}")
                        
                        # If we have optimized data, prioritize it and break
                        if 'optimized' in filename and filename.endswith('.parquet'):
                            break
                    else:
                        missing_cols = [col for col in required_cols if col not in df.columns]
                        print(f"⚠️  Skipping {filename}: missing columns {missing_cols}")
                        
                except Exception as e:
                    print(f"❌ Error loading {filename}: {e}")
                    continue
        
        if not combined_data:
            print("❌ No valid data files found")
            return False
        
        # If we only have one source loaded, try to get 2025 data separately
        if len(loaded_years) == 1 and '2025' not in loaded_years:
            print("🔍 Looking for 2025 data...")
            for source in data_sources:
                if source['year'] == '2025' and os.path.exists(source['file']):
                    try:
                        print(f"📊 Adding 2025 data from {source['file']}...")
                        df_2025 = pd.read_csv(source['file'], nrows=7500)  # Half the limit for balance
                        df_2025['Data_Year'] = '2025'
                        
                        if 'Employer_Name' in df_2025.columns and 'State' in df_2025.columns:
                            combined_data.append(df_2025)
                            loaded_years.add('2025')
                            print(f"✅ Added {len(df_2025):,} records from 2025")
                            break
                    except Exception as e:
                        print(f"❌ Error loading 2025 data: {e}")
        
        # Combine all data
        if len(combined_data) == 1:
            self.data = combined_data[0]
        else:
            print("🔗 Combining data from multiple sources...")
            self.data = pd.concat(combined_data, ignore_index=True)
        
        # Optimize dtypes
        categorical_cols = ['State', 'City', 'Data_Year']
        for col in categorical_cols:
            if col in self.data.columns:
                self.data[col] = self.data[col].astype('category')
        
        years_loaded = sorted(list(loaded_years))
        print(f"✅ Total: {len(self.data):,} records from years {years_loaded}")
        return True
    
    def get_filter_options(self):
        """Get filter options from loaded data."""
        if self.data is None:
            return [], [], [], [], []
        
        # States - ensure no duplicates and proper sorting
        states = sorted(list(set(self.data['State'].dropna().astype(str).tolist())))
        
        # Cities - use ONLY data-extracted cities with proper normalization and alphabetical sorting
        if 'City' in self.data.columns and 'State' in self.data.columns:
            # Create city, state combinations from actual data with normalization
            valid_mask = (
                self.data['City'].notna() & 
                self.data['State'].notna() &
                (self.data['City'].astype(str).str.strip() != '') &
                (self.data['State'].astype(str).str.strip() != '')
            )
            
            if valid_mask.sum() > 0:
                valid_data = self.data[valid_mask]
                
                # Normalize city-state combinations to handle case inconsistencies
                normalized_combos = []
                for _, row in valid_data.iterrows():
                    # Normalize: Title Case for city, Upper Case for state, strip whitespace
                    city_clean = str(row['City']).strip().title()
                    state_clean = str(row['State']).strip().upper()
                    
                    # Skip ZIP codes (numeric-only cities) - they shouldn't be in city list
                    if city_clean.isdigit():
                        continue
                        
                    normalized_combo = f"{city_clean}, {state_clean}"
                    normalized_combos.append(normalized_combo)
                
                # Count occurrences and get unique cities
                from collections import Counter
                combo_counts = Counter(normalized_combos)
                
                # Sort alphabetically (not by frequency) and take top 50
                cities = sorted(combo_counts.keys())[:50]
            else:
                cities = []
        else:
            cities = []
        
        # Classifications
        classifications = []
        if 'Classifications' in self.data.columns:
            all_class = []
            for c in self.data['Classifications'].dropna():
                if pd.notna(c):
                    all_class.extend([x.strip() for x in str(c).split(',')])
            classifications = sorted(list(set(all_class)))[:20]  # Top 20
        
        # Pre-defined options
        industries = ['Technology', 'Healthcare', 'Education', 'Government', 'Research']
        sizes = ['Small (1-25)', 'Medium (26-100)', 'Large (101-500)', 'Enterprise (500+)']
        
        return states, cities, classifications, industries, sizes
    
    def search_employers(self, search_text, states, cities, classifications, 
                        min_score, min_approval, only_cap_exempt, year_filter='All Years'):
        """Fast search function with automatic deduplication."""
        if self.data is None:
            return pd.DataFrame(), "❌ No data available", None
        
        df = self.data.copy()
        
        # Apply filters
        if search_text:
            mask = df['Employer_Name'].str.contains(search_text, case=False, na=False)
            df = df[mask]
        
        if states:
            df = df[df['State'].isin(states)]
        
        if cities:
            # Handle city filtering with normalized "City, State" format
            city_state_conditions = []
            for city_state in cities:
                if ', ' in city_state:
                    city, state = city_state.rsplit(', ', 1)
                    # Create condition that matches normalized format
                    condition = (
                        (df['City'].astype(str).str.strip().str.title() == city.strip()) & 
                        (df['State'].astype(str).str.strip().str.upper() == state.strip())
                    )
                    city_state_conditions.append(condition)
            
            if city_state_conditions:
                city_filter = city_state_conditions[0]
                for condition in city_state_conditions[1:]:
                    city_filter = city_filter | condition
                df = df[city_filter]
        
        # Handle organization type filtering with mapping
        if classifications and 'Classifications' in df.columns:
            # Map user-friendly categories to actual data classifications
            classification_mapping = {
                '🎓 Universities & Colleges': ['university', 'education'],
                '🏥 Hospitals & Medical Centers': ['hospital', 'Hospital'],
                '🔬 Research Organizations': ['research_org', 'Research'],
                '🏛️ Government Agencies': ['government', 'Government'],
                '📚 Educational Institutions': ['education', 'university'],
                '🩺 Healthcare Systems': ['healthcare', 'hospital'],
                '💼 Professional Services': ['professional_services'],
                '🏢 Non-profit Organizations': ['nonprofit']
            }
            
            # Build filter for selected categories
            matching_keywords = []
            for selected_category in classifications:
                if selected_category in classification_mapping:
                    matching_keywords.extend(classification_mapping[selected_category])
            
            if matching_keywords:
                # Filter rows where Classifications contains any of the matching keywords
                mask = df['Classifications'].fillna('').str.lower().str.contains(
                    '|'.join(matching_keywords), case=False, na=False
                )
                df = df[mask]
        
        if only_cap_exempt and 'Likely_Cap_Exempt' in df.columns:
            df = df[df['Likely_Cap_Exempt'] == True]
        
        if 'Cap_Exempt_Score' in df.columns:
            df = df[df['Cap_Exempt_Score'] >= min_score]
        
        if 'Approval_Rate' in df.columns:
            df = df[df['Approval_Rate'] >= min_approval]
        
        # Filter by year
        if year_filter != 'All Years' and 'Data_Year' in df.columns:
            df = df[df['Data_Year'] == year_filter]
        
        # Remove duplicate employers by default (keep the best record)
        if len(df) > 0:
            # Create a more robust normalized employer name for deduplication
            df['employer_clean'] = (df['Employer_Name']
                                   .str.strip()
                                   .str.upper()
                                   .str.replace(r'[^\w\s]', '', regex=True)  # Remove punctuation
                                   .str.replace(r'\s+', ' ', regex=True))    # Normalize spaces
            
            # Sort to prioritize the best records (highest scores first)
            sort_cols = []
            if 'Cap_Exempt_Score' in df.columns:
                sort_cols.append('Cap_Exempt_Score')
            if 'Approval_Rate' in df.columns:
                sort_cols.append('Approval_Rate')
            if 'Total_Petitions' in df.columns:
                sort_cols.append('Total_Petitions')
            
            if sort_cols:
                df = df.sort_values(sort_cols, ascending=False)
            
            # Keep only the first (best) record for each employer
            df = df.drop_duplicates(subset=['employer_clean'], keep='first')
            df = df.drop(columns=['employer_clean'])  # Remove helper column
        
        # Format results with better column names
        display_cols = []
        col_mapping = {
            'Employer_Name': 'Employer Name',
            'City': 'City', 
            'State': 'State',
            'Cap_Exempt_Score': 'Cap-Exempt Score',
            'Approval_Rate': 'Approval Rate',
            'Total_Petitions': 'Total Petitions',
            'Data_Year': 'Year'
        }
        
        for col in ['Employer_Name', 'City', 'State', 'Cap_Exempt_Score', 'Approval_Rate', 'Total_Petitions', 'Data_Year']:
            if col in df.columns:
                display_cols.append(col)
        
        # Add default sorting: Company name ascending, Total petitions descending
        sort_columns = []
        if 'Employer_Name' in df.columns:
            sort_columns.append('Employer_Name')
        if 'Total_Petitions' in df.columns:
            sort_columns.append('Total_Petitions')
        
        if sort_columns:
            if len(sort_columns) == 2:
                # Sort by employer name (ascending), then total petitions (descending)
                df_sorted = df.sort_values([sort_columns[0], sort_columns[1]], ascending=[True, False])
            else:
                df_sorted = df.sort_values(sort_columns[0], ascending=True)
            result_df = df_sorted[display_cols].head(100)
        else:
            result_df = df[display_cols].head(100)
        
        # Store year data before renaming columns
        years_in_results = result_df['Data_Year'].unique().tolist() if 'Data_Year' in result_df.columns else ['N/A']
        states_in_results = len(result_df['State'].unique()) if 'State' in result_df.columns else 0
        
        # Rename columns for better display
        result_df = result_df.rename(columns=col_mapping)
        
        # Round numeric columns for cleaner display
        for col in ['Cap-Exempt Score', 'Approval Rate']:
            if col in result_df.columns:
                result_df[col] = result_df[col].round(3)
        
        # Create summary
        total_found = len(df)
        showing = min(100, total_found)
        
        summary = f"""
        ## 📊 Search Results
        
        **Found {total_found:,} unique employers matching your criteria**
        
        - 📋 **Displaying:** {showing:,} of {total_found:,} results{' (top matches)' if total_found > 100 else ''}
        - 📍 **States/Territories:** {states_in_results} (in displayed results)
        - 📅 **Data Year:** {sorted(years_in_results)}
        - 🔄 **Auto-deduplicated:** Best record kept per employer
        
        💡 **Tip:** These employers can sponsor H-1B visas year-round!
        """
        
        # Create simple chart
        chart = None
        if len(result_df) > 0 and 'State' in result_df.columns:
            state_counts = result_df['State'].value_counts().head(10)
            chart = px.bar(
                x=state_counts.values, 
                y=state_counts.index, 
                orientation='h',
                title=f'📊 Top 10 States/Territories ({len(result_df)} employers)',
                labels={'x': 'Count', 'y': 'State'}
            )
            chart.update_layout(height=400)
        
        return result_df, summary, chart

def create_fast_interface():
    """Create optimized interface with instant loading."""
    print("🚀 Creating fast interface...")
    
    # Pre-define filter options for immediate display
    all_states = [
        'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'GU', 'HI', 
        'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 
        'MP', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 
        'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA', 
        'WI', 'WV', 'WY'
    ]
    
    top_cities = [
        'New York, NY', 'Los Angeles, CA', 'Chicago, IL', 'Houston, TX', 'Philadelphia, PA',
        'Phoenix, AZ', 'San Antonio, TX', 'San Diego, CA', 'Dallas, TX', 'San Jose, CA',
        'Austin, TX', 'Jacksonville, FL', 'Fort Worth, TX', 'Columbus, OH', 'Charlotte, NC',
        'San Francisco, CA', 'Indianapolis, IN', 'Seattle, WA', 'Denver, CO', 'Washington, DC',
        'Boston, MA', 'El Paso, TX', 'Nashville, TN', 'Detroit, MI', 'Oklahoma City, OK',
        'Portland, OR', 'Las Vegas, NV', 'Memphis, TN', 'Louisville, KY', 'Baltimore, MD',
        'Milwaukee, WI', 'Albuquerque, NM', 'Tucson, AZ', 'Fresno, CA', 'Sacramento, CA',
        'Mesa, AZ', 'Kansas City, MO', 'Atlanta, GA', 'Long Beach, CA', 'Colorado Springs, CO',
        'Raleigh, NC', 'Miami, FL', 'Virginia Beach, VA', 'Omaha, NE', 'Oakland, CA',
        'Minneapolis, MN', 'Tulsa, OK', 'Arlington, TX', 'Tampa, FL', 'New Orleans, LA'
    ]
    
    # Simplified and consolidated organization types based on actual data
    org_types = [
        '🎓 Universities & Colleges',
        '🏥 Hospitals & Medical Centers', 
        '🔬 Research Organizations',
        '🏛️ Government Agencies',
        '📚 Educational Institutions',
        '🩺 Healthcare Systems',
        '💼 Professional Services',
        '🏢 Non-profit Organizations'
    ]
    
    dashboard = FastJobSeekerDashboard()
    
    if dashboard.data is None:
        with gr.Blocks() as demo:
            gr.Markdown("❌ Could not load data files. Please check your setup.")
        return demo
    
    # Try to get actual filter options, but use pre-defined as fallback
    try:
        states, cities, classifications, industries, sizes = dashboard.get_filter_options()
        print(f"✅ Interface ready: {len(states)} states/territories, {len(cities)} cities")
    except:
        states, cities, classifications = all_states, top_cities, org_types
        industries = ['Technology', 'Healthcare', 'Education', 'Government', 'Research']
        sizes = ['Small (1-25)', 'Medium (26-100)', 'Large (101-500)', 'Enterprise (500+)']
        print(f"✅ Interface ready with pre-defined options")
    
    with gr.Blocks(
        title="Job Seeker Dashboard - H-1B Cap-Exempt Employers",
        css="""
        /* Disable autofill/autocomplete on iOS Safari */
        #search_box input, 
        #state_filter input,
        #city_filter input,
        #classification_filter input,
        select {
            -webkit-text-security: none !important;
            -webkit-autofill: none !important;
            autocomplete: off !important;
            -webkit-contact-autofill-disabled: true !important;
        }
        
        /* Additional iOS Safari fixes */
        input[type="text"],
        input[type="search"],
        select {
            autocomplete: off;
            autocorrect: off;
            autocapitalize: off;
            spellcheck: false;
        }
        
        /* Better table column sizing */
        .dataframe table {
            table-layout: auto !important;
            width: 100% !important;
        }
        
        .dataframe th, .dataframe td {
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            min-width: 80px !important;
        }
        
        /* Make manual search button less prominent */
        .secondary {
            opacity: 0.7 !important;
        }
        """
    ) as demo:
        
        gr.Markdown("""
        # 🎯 Job Seeker Dashboard: Cap-Exempt H-1B Employers
        
        **Find employers who can sponsor H-1B visas year-round!**
        
        ✅ **Multi-Year Data:** 2024 & 2025 employers ready for instant search
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 🔍 Search Filters")
                
                search_box = gr.Textbox(
                    label="🏢 Company Name Search",
                    placeholder="Enter company keywords...",
                    value="",
                    elem_id="search_box"
                )
                
                state_filter = gr.Dropdown(
                    choices=states,
                    label="📍 States & Territories",
                    multiselect=True,
                    value=[],
                    info=f"50 US states + DC + territories ({len(states)} total)",
                    elem_id="state_filter"
                )
                
                city_filter = gr.Dropdown(
                    choices=cities,
                    label="🏙️ Cities (Alphabetical)",
                    multiselect=True,
                    value=[],
                    info=f"Top {len(cities)} cities alphabetically sorted (normalized, no duplicates)",
                    elem_id="city_filter"
                )
                
                classification_filter = gr.Dropdown(
                    choices=classifications,
                    label="🏢 Organization Categories",
                    multiselect=True,
                    value=[],
                    info="Choose from consolidated categories with emojis",
                    elem_id="classification_filter"
                )
                
                score_slider = gr.Slider(
                    minimum=0, maximum=1, value=0.6, step=0.1,
                    label="🎯 Min Cap-Exempt Score"
                )
                
                approval_slider = gr.Slider(
                    minimum=0, maximum=1, value=0.7, step=0.1,
                    label="✅ Min Approval Rate"
                )
                
                cap_exempt_only = gr.Checkbox(
                    label="📋 Only show likely cap-exempt employers",
                    value=True
                )
                
                year_filter = gr.Dropdown(
                    choices=['All Years', '2024', '2025'],
                    label="📅 Data Year",
                    value='All Years',
                    info="Filter by specific year or show all data"
                )
                
                gr.Markdown("**ℹ️ Note:** Duplicate employers are automatically removed, keeping the best record for each company.")
                
                with gr.Accordion("🔧 Advanced Options", open=False):
                    search_btn = gr.Button("🔍 Manual Search", variant="secondary", size="sm")
                    gr.Markdown("*Use manual search if auto-filtering stops working*")
            
            with gr.Column(scale=2):
                summary_display = gr.Markdown("🔄 **Auto-search enabled!** Results update instantly when you adjust filters.")
                results_table = gr.Dataframe(
                    label="📊 Search Results", 
                    interactive=False,
                    wrap=True
                )
        
        chart_display = gr.Plot(label="📈 Geographic Distribution")
        
        # Define search inputs and outputs for reuse
        search_inputs = [
            search_box, state_filter, city_filter, classification_filter,
            score_slider, approval_slider, cap_exempt_only, year_filter
        ]
        search_outputs = [results_table, summary_display, chart_display]
        
        # Auto-search when any filter changes
        search_box.change(
            fn=dashboard.search_employers,
            inputs=search_inputs,
            outputs=search_outputs
        )
        
        state_filter.change(
            fn=dashboard.search_employers,
            inputs=search_inputs,
            outputs=search_outputs
        )
        
        city_filter.change(
            fn=dashboard.search_employers,
            inputs=search_inputs,
            outputs=search_outputs
        )
        
        classification_filter.change(
            fn=dashboard.search_employers,
            inputs=search_inputs,
            outputs=search_outputs
        )
        
        score_slider.change(
            fn=dashboard.search_employers,
            inputs=search_inputs,
            outputs=search_outputs
        )
        
        approval_slider.change(
            fn=dashboard.search_employers,
            inputs=search_inputs,
            outputs=search_outputs
        )
        
        cap_exempt_only.change(
            fn=dashboard.search_employers,
            inputs=search_inputs,
            outputs=search_outputs
        )
        
        year_filter.change(
            fn=dashboard.search_employers,
            inputs=search_inputs,
            outputs=search_outputs
        )
        
        # Keep manual search button as backup
        search_btn.click(
            fn=dashboard.search_employers,
            inputs=search_inputs,
            outputs=search_outputs
        )
        
        # Auto-search on Enter in search box
        search_box.submit(
            fn=dashboard.search_employers,
            inputs=search_inputs,
            outputs=search_outputs
        )
        
        # Load initial results when the interface starts
        demo.load(
            fn=dashboard.search_employers,
            inputs=search_inputs,
            outputs=search_outputs
        )
        
        gr.Markdown("""
        ---
        ### 💡 About Cap-Exempt H-1B Employers
        
        **These employers can file H-1B petitions ANYTIME - no lottery required!**
        
        - 🎓 **Universities & Colleges** - Public and private higher education
        - 🏥 **Teaching Hospitals** - Medical centers affiliated with universities  
        - 🏛️ **Government Agencies** - Federal, state, and local government
        - 🔬 **Research Organizations** - Nonprofit research institutes
        
        **🎯 Perfect for:** International students, current H-1B holders looking to switch, professionals seeking year-round opportunities
        """)
    
    return demo

def main():
    """Launch the fast dashboard."""
    print("🚀 Starting Fast Job Seeker Dashboard...")
    
    try:
        demo = create_fast_interface()
        print("✅ Fast dashboard ready!")
        
        demo.launch(
            share=False,
            server_name="0.0.0.0",
            server_port=7860,
            show_error=True
        )
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 