public class DataItem {
    private String key;
    private String description;
    private DataItem next = null;
    private int index = -1;

    public DataItem(String key) {
        this.key = key;
        this.description = "";
    }

    public DataItem(String key, String description) {
        this.key = key;
        this.description = description;
    }

    public String getKey() {
        return key;
    }

    public void setKey(String key) {
        this.key = key;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public DataItem getNext() {
        return next;
    }

    public void setNext(DataItem next) {
        this.next = next;
    }

    public int getIndex() {
        return index;
    }

    public void setIndex(int index) {
        this.index = index;
    }
}