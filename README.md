---
title: Job Seeker Dashboard - Cap-Exempt H-1B Employers
emoji: 🎯
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
---

# 🎯 H-1B Cap-Exempt Job Seeker Dashboard

**Find employers who can sponsor H-1B visas year-round - no lottery required!**

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/Andrew-Ulloa/job-seeker-dashboard-v2)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Gradio](https://img.shields.io/badge/gradio-4.0+-orange.svg)](https://gradio.app/)

## 🌟 Features

### ✅ **Multi-Year Data Coverage**

- **2024 & 2025** H-1B employer data
- 22,500+ unique employers ready for instant search
- Real-time filtering and search capabilities

### 🔍 **Advanced Search & Filtering**

- **Instant Search**: Results update as you type
- **Geographic Filters**: States, territories, and cities (alphabetically sorted)
- **Organization Categories**: Universities, hospitals, research orgs, government
- **Smart Deduplication**: Best record kept per employer
- **Score-based Filtering**: Cap-exempt likelihood and approval rates

### 🎨 **Modern UI/UX**

- **Auto-filtering**: No search button needed
- **Responsive Design**: Works on desktop and mobile
- **Interactive Charts**: Geographic distribution visualization
- **Collapsible Tables**: Clean, organized data display

### 🚀 **Performance Optimized**

- **Fast Loading**: Optimized data structures
- **Efficient Filtering**: Real-time updates without lag
- **Smart Caching**: Reduced memory footprint

## 🏢 Cap-Exempt Employer Types

These employers can file H-1B petitions **anytime** - no lottery required:

- 🎓 **Universities & Colleges** - Public and private higher education
- 🏥 **Teaching Hospitals** - Medical centers affiliated with universities
- 🏛️ **Government Agencies** - Federal, state, and local government
- 🔬 **Research Organizations** - Nonprofit research institutes

## 🚀 Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/Andrew-Ulloa/job-seeker-dashboard-v2.git
cd job-seeker-dashboard-v2

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Hugging Face Spaces

The dashboard is automatically deployed to Hugging Face Spaces on every commit to main branch.

**Live Demo**: https://huggingface.co/spaces/Andrew-Ulloa/job-seeker-dashboard-v2

## 📊 Data Sources

- **LCA Disclosure Data**: Department of Labor H-1B petitions
- **Cap-Exempt Analysis**: Machine learning classification
- **Multi-year Coverage**: 2024-2025 data combined
- **Quality Assurance**: Automated deduplication and validation

## 🛠️ Technical Stack

- **Frontend**: Gradio 4.0+ (Python web framework)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly Express
- **Deployment**: Hugging Face Spaces
- **CI/CD**: GitHub Actions → HF Spaces auto-sync

## 📈 Recent Improvements

### v2.0 Features

- ✅ **Alphabetical City Sorting**: Cities now sorted A-Z for better UX
- ✅ **Case Normalization**: Eliminates duplicates like "NEW YORK" vs "New York"
- ✅ **Enhanced Filtering**: Improved city-state matching logic
- ✅ **UI Polish**: Better labels and descriptions
- ✅ **Performance**: Faster loading and filtering

### Previous Versions

- Auto-filtering dashboard with instant search
- Organization type consolidation with emojis
- Multi-year data integration
- Collapsible table interface

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Perfect For

- **International Students**: Find year-round sponsorship opportunities
- **H-1B Holders**: Discover employers for job switches
- **Career Professionals**: Explore cap-exempt career paths
- **Recruiters**: Identify potential employer partners

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Andrew-Ulloa/job-seeker-dashboard-v2/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Andrew-Ulloa/job-seeker-dashboard-v2/discussions)
- **Live Demo**: [Hugging Face Space](https://huggingface.co/spaces/Andrew-Ulloa/job-seeker-dashboard-v2)

---

**⭐ Star this repository if it helps you find your next opportunity!**

_This tool is for informational purposes only. Always verify cap-exempt status with employers and immigration attorneys._
